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
| **Đề tài chính** | **[`degron-footprint`](topics/degron-footprint/README.md)** — footprint / hiệu ứng đột biến degron mức residue | [D-023](#d-023) |
| **Dự phòng** | **[`plm-calibration-audit`](topics/plm-calibration-audit/README.md)** (A4) — audit calibration và miền áp dụng | [D-023](#d-023) |
| Đang đào sâu (5, vị trí chưa quyết) | [xai-fidelity-benchmark](topics/xai-fidelity-benchmark/README.md) (A2) · [structure-sequence-leakage-audit](topics/structure-sequence-leakage-audit/README.md) (A3) · [dark-kinome-zero-shot](topics/dark-kinome-zero-shot/README.md) · [budgeted-plm-variant-scoring](topics/budgeted-plm-variant-scoring/README.md) · [scalable-metagenomic-binning](topics/scalable-metagenomic-binning/README.md) | [D-019](#d-019), [D-023](#d-023), C-4 |
| Thứ tự tiềm năng | Là **số đầu tên thư mục** trong `topics/` (ví dụ `1-ten-de-tai`), do Trọng tự đặt. **Chưa đặt** | [D-019](#d-019) |
| Định hướng chọn đề tài | 1) ưu tiên tin sinh học; 2) không bó vào dự đoán residue/peptide; 3) ưu tiên tầng công cụ/benchmark/nền tảng; 4) đề tài ngoài tin sinh học vẫn hợp lệ nhưng xếp sau. Mức 3 **đã được GVHD xác nhận là hợp lệ** | [D-017](#d-017), [D-022](#d-022) |
| Đóng góp dạng công cụ | **GVHD chấp nhận** (công cụ, thước đo, audit, benchmark, thuật toán tối ưu). Vẫn phải là đóng góp **dương** đo được | [D-022](#d-022), [D-012](#d-012) |
| Thước đo một ứng viên | 5 tiêu chí GVHD + 3 cổng bắt buộc G1/G2/G3, xem [course.md](project/course.md) | [D-006](#d-006), [D-012](#d-012) |
| Đã đóng (lưu trữ) | RCA, RTK–ATP, TME senescence, cơ chất sirtuin, legal QA, quản lý chi tiêu, efflux, IL-6, sửa lỗi phần mềm. Xem [archive/](archive/README.md) | D-003, D-006, D-008, D-010, D-011, D-019, [D-021](#d-021) |
| Quy ước đang áp dụng | HTML để trong repo, không dùng artifact ([D-013](#d-013)). Repo private ([D-004](#d-004)) | — |

**Mốc tiếp theo:** tuần 6 báo cáo lại đề tài với GVHD (xem [course.md](project/course.md)) — trình `degron-footprint`.

**Việc chặn gần nhất của đề tài chính:** Trọng xác nhận **C-6** (bảy đề xuất từ audit dữ liệu 13/10, gồm mốc đánh giá G2 và nguồn nhãn chính). Việc chặn trước đó — tính lực thống kê trên tập test 221–322 footprint — **đã xong 13/10: đủ lực**. Xem [thẻ đề tài](topics/degron-footprint/README.md) và [báo cáo audit](topics/degron-footprint/research/full-data-audit/README.md).

---

## C. Đề xuất chờ Trọng xác nhận

| # | Đề xuất | Người đề xuất | Ghi chú |
|---|---|---|---|
| C-2 | Thứ tự giữa A2 và A3 | Claude, 12/10/2026 | Phần A4 của đề xuất này **đã được giải quyết** — A4 là dự phòng theo [D-023](#d-023). Còn lại thứ tự A2 ↔ A3, chỉ là gợi ý trong [deep-dive](topics/plm-calibration-audit/research/deep-dive-2026-10-12.md). Thay bằng số đầu tên thư mục khi Trọng đặt |
| C-4 | Năm ứng viên còn lại giữ trong `topics/` hay đóng bớt: A2, A3, `dark-kinome-zero-shot`, `budgeted-plm-variant-scoring`, `scalable-metagenomic-binning` | Claude, 12/10/2026 | [D-023](#d-023) đã quyết đề tài chính và dự phòng, nhưng **chưa quyết** số phận năm ứng viên này; chúng đang giữ nguyên trạng. Giữ cả năm thì tốn công theo dõi; `dark-kinome-zero-shot` có G2 yếu nhất (trụ tính mới đã sụp) nên là ứng viên đóng trước. Đối chiếu: [khảo sát 7 ứng viên](surveys/seven-candidates-comparison-2026-10-12.md) |
| C-6 | **Bảy đề xuất từ audit dữ liệu đầy đủ của `degron-footprint`** (13/10), xem [báo cáo §9](topics/degron-footprint/research/full-data-audit/README.md): **(1)** sửa cách phát biểu mục tiêu G2 — bỏ "vượt 0,6045 / +28,9%", dùng baseline thành phần trung thực **0,4897** làm mốc và báo kèm trần nhãn **0,6514**, vì 0,6045 và 0,7792 đều là oracle đọc nhãn test; **(2)** chuyển trọng tâm nhãn sang **bộ bão hòa** (nhiễu 16,7% so với 75,9%, Jaccard 0,66 so với 0,50, ma trận phủ 97,9%) và nhận rủi ro chỉ 235 peptide; **(3)** dùng nhãn trung bình hai replicate thay vì một; **(4)** chọn split cụm protein **cov80** thay cov50 để lực đạt 0,92–0,94; **(5)** giữ 130 peptide có cả hai nguồn nhãn cùng phía train/test; **(6)** nêu SVM của Zhang 2023 trong G3 và đề cương, làm rõ khác phạm vi peptide/residue; **(7)** không trộn mẫu BAG6 WT với hai replicate kia | Claude, 13/10/2026 | Đề xuất (1) và (2) đổi mốc đánh giá và nguồn nhãn chính của đề tài nên **cần Trọng quyết**, không tự áp. Việc chặn cũ ("tính lực thống kê") **đã xong**: tập test 221–322 đủ lực. Thẻ đề tài đã sửa phần **bằng chứng đo được**; phần **mốc cam kết** vẫn chờ mục này |
| C-5 | Xác nhận lại với GVHD ở tuần 6 rằng đóng góp dạng công cụ được nhận | Claude, 12/10/2026 | [D-022](#d-022) dựa trên thông tin Trọng truyền đạt, **chưa có biên bản**, và nó đọc lại lời GVHD ngày 11/10 theo hướng nhẹ hơn. Nên hỏi một câu xác nhận để khỏi phải đổi hướng muộn |

---

## B. Sổ quyết định (mới nhất ở trên)

Trường "Ai quyết": **Trọng** (sinh viên), **GVHD**, **Claude (ủy quyền)** — Trọng giao cho Claude tự quyết, **Claude (khuyến nghị)** — chỉ là khuyến nghị nhưng đã được dùng như quyết định.

### D-023
**12/10/2026 · Trọng · Hiệu lực.** **Đề tài chính là [`degron-footprint`](topics/degron-footprint/README.md)** (dự đoán footprint / hiệu ứng đột biến degron mức residue trên nhãn thực nghiệm). **Dự phòng là [`plm-calibration-audit`](topics/plm-calibration-audit/README.md)** (A4, công cụ audit calibration và miền áp dụng). Thay vị trí đề tài chính ở [D-021](#d-021) ("chưa có đề tài chính") và vị trí dự phòng ở [D-016](#d-016) (degron là dự phòng duy nhất); giải quyết đề xuất C-4 phần đề tài chính/dự phòng.

Lý do: degron là ứng viên duy nhất có **khoảng trống đã chứng minh** chứ không phải "chưa kiểm" — 2.353/2.624 peptide (89,7%) có nhóm cùng cặp thay thế chứa cả vị trí dương và không dương, nên mô hình chỉ dùng thành phần amino acid **bị chứng minh không tách được**; cận trên chính xác của lớp mô hình đó là precision@3 0,6045, oracle không ràng buộc 0,7792 ([audit](topics/degron-footprint/research/composition-context-audit.md)). Thêm vào đó: G1 mạnh nhất repo, TC4 (XAI) được thỏa mãn bởi chính bài toán vì đầu ra là điểm quan trọng theo residue, có kiến trúc để đề xuất (mục 6 của audit), và dữ liệu đã nằm trên máy nên khả thi trong 8–9 tuần còn lại. A4 làm dự phòng vì G2 ít phụ thuộc kết quả âm nhất trong nhóm công cụ và G3 tự nhiên nhất, nay đã hợp lệ theo [D-022](#d-022).

**Chưa quyết (vẫn ở phần C):** vị trí của năm ứng viên còn lại — A2, A3, `dark-kinome-zero-shot`, `budgeted-plm-variant-scoring`, `scalable-metagenomic-binning`. Chúng giữ nguyên trạng "đang đào sâu" cho tới khi Trọng nói khác.

### D-022
**12/10/2026 · GVHD (Trọng truyền đạt) · Hiệu lực.** **GVHD chấp nhận đóng góp dạng công cụ** (công cụ, thước đo, audit, benchmark, thuật toán tối ưu) làm đóng góp của luận văn. Giải quyết đề xuất C-3 theo hướng thuận và **gỡ rào** cho các ứng viên A2, A3, A4, `budgeted-plm-variant-scoring`, `scalable-metagenomic-binning`.

Hệ quả: mức 3 của [D-017](#d-017) (ưu tiên tầng công cụ/benchmark/nền tảng) không còn mâu thuẫn với kỳ vọng của GVHD. Lời GVHD ngày 11/10 ("kỳ vọng một kiến trúc chưa ai dùng") vì vậy được đọc là **mong muốn, không phải điều kiện loại**; cả hai lời được giữ nguyên văn ở [people.md](project/people.md). Vẫn nên xác nhận lại ở buổi gặp tuần 6, vì đây là thông tin Trọng truyền đạt, chưa có biên bản.

Lưu ý điều **không** thay đổi: cổng [G2](project/course.md) vẫn đòi một đóng góp **dương** đo được — GVHD nhận dạng công cụ không có nghĩa là nhận kết quả âm ([D-012](#d-012)). Tiêu chí 5 (ứng dụng/website) vẫn không thể thiếu ([D-006](#d-006)).

### D-021
**12/10/2026 · Trọng · Hiệu lực; phần "chưa có đề tài chính" bị thay bởi [D-023](#d-023).** Lưu trữ đề tài `budgeted-microservice-rca` tại [archive/topics/budgeted-microservice-rca/](archive/topics/budgeted-microservice-rca/README.md), giữ toàn bộ tài liệu, code và dữ liệu đã có. **Hiện chưa có đề tài chính.** Thay vị trí đề tài chính ở D-016 và phần giữ RCA trong nhóm đang đào sâu ở D-019; giải quyết đề xuất C-1. Các nội dung còn lại của D-016 và D-019 giữ hiệu lực.

### D-020
**12/10/2026 · Trọng · Hiệu lực.** Bỏ thư mục `data/` ở gốc. Dữ liệu của mỗi đề tài nằm trong chính thư mục đề tài, ở `topics/<ten-de-tai>/data/` (đề tài đã đóng: `archive/topics/<ten-de-tai>/data/`), và bị `.gitignore` chặn. Dữ liệu của đề tài đã đóng được giữ, không xoá.

### D-019
**12/10/2026 · Trọng · Hiệu lực; phần giữ RCA trong nhóm đang đào sâu bị thay bởi [D-021](#d-021).** Tổ chức lại repo. Từ nay quyết định chỉ ghi ở file này. Sáu đề tài đang đào sâu có thư mục riêng trong `topics/`: RCA, A2, A3, A4, degron, dark kinome zero-shot (mở lại hướng này). **Đóng hai đề tài không liên quan tin sinh học**: `legal-qa-grounding` và `personal-expense-management`. RCA vẫn giữ trong `topics/`. Các hướng cũ chuyển vào `archive/`. Thứ tự tiềm năng được mã hóa bằng số đầu tên thư mục, do Trọng tự đặt.

### D-018
**12/10/2026 (tối) · Trọng · Hiệu lực.** Từ 14 ứng viên tầng công cụ trong [khảo sát](surveys/bioinformatics-tool-layer-candidates-2026-10-12.md), đi sâu ba ứng viên bậc A khớp GVHD: A2 (fidelity XAI), A3 (cấu trúc + trình tự, **phải thu hẹp** thành audit vì đã có Denger & Helms 2025), A4 (calibration/miền áp dụng). Nguồn: [journal 12/10](journal/2026-10.md).

### D-017
**12/10/2026 · Trọng · Hiệu lực.** Định hướng chọn đề tài có 4 mức, tóm tắt ở phần A. Mục tiêu tối cao là tìm một đề tài có đóng góp thật, giải quyết vấn đề có ý nghĩa. Mục tiêu này đứng trên độ khớp với các ứng viên đang có.

### D-016
**12/10/2026 (chiều) · Claude (ủy quyền: "Claude tự quyết toàn bộ, chốt trong ngày") · Vị trí đề tài chính bị thay bởi [D-021](#d-021); vị trí dự phòng bị thay bởi [D-023](#d-023).** Chọn `budgeted-microservice-rca` làm đề tài chính, thay [D-014](#d-014). Degron là dự phòng duy nhất. Căn cứ: [báo cáo lựa chọn mở lĩnh vực](surveys/open-field-topic-selection-2026-10-12.md).

### D-015
**12/10/2026 · Trọng · Bị thay bởi D-016, đóng ở D-019.** Đưa `legal-qa-grounding` (hỏi–đáp pháp luật tiếng Việt) lên làm ứng viên hàng đầu ngoài lĩnh vực.

### D-014
**11/10/2026 · Trọng · Bị thay bởi D-016.** Chốt degron làm đề tài chính. (Degron trở lại vị trí đề tài chính theo [D-023](#d-023), **không phải** vì mục này còn hiệu lực.) Khuya cùng ngày tái định tâm: bỏ trục đặc hiệu E3 (chỉ 1 E3 đủ mẫu), chuyển sang dự đoán footprint mức residue trên nhãn đột biến. Slug cũ `degron-e3-specificity`, nay là `degron-footprint`.

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
