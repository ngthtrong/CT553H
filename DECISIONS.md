# Quyết định của dự án — nơi duy nhất

> **Quy tắc.** Đây là **file duy nhất** ghi quyết định đã chốt. Mọi tài liệu khác (báo cáo, nhật ký, thẻ đề tài, biên bản) chỉ được **dẫn link** tới đây (`DECISIONS.md#d-0xx`), không tự viết "đã chốt / quyết định". Câu "chốt" trong tài liệu cũ là **lịch sử**, không có hiệu lực nếu không khớp phần A.
>
> - **Phần A** ghi trạng thái hiện hành, dài tối đa một màn hình. Khi có thay đổi thì **sửa đè**, không cộng dồn.
> - **Phần B** là sổ quyết định. Thêm mục mới **lên đầu**. Mục cũ không xoá: chỉ đổi trạng thái thành `Bị thay bởi D-0yy`.
> - **Phần C** chứa đề xuất **chưa được Trọng xác nhận**. Đề xuất của Claude chỉ chuyển sang phần B khi Trọng đồng ý.

---

## A. Hiện hành — cập nhật 15/10/2026

| Mục | Giá trị | Căn cứ |
|---|---|---|
| Giai đoạn | Chọn và hoàn thiện đề tài. **Chưa có đề tài nào được GVHD duyệt**; chưa huấn luyện mô hình hay xây ứng dụng | — |
| **Đề tài chính** | **[`degron-footprint`](topics/degron-footprint/README.md)** — footprint / hiệu ứng đột biến degron mức residue. Mạch lập luận hiện hành: [topic-argument-2026-10-15.md](topics/degron-footprint/research/topic-argument-2026-10-15.md) | [D-023](#d-023) |
| **Dự phòng** | **Chưa có.** `plm-calibration-audit` (A4) đã lưu trữ theo [D-024](#d-024); có thể mở lại từ `archive/` nếu cần | [D-024](#d-024) |
| Đang đào sâu | Không còn đề tài nào ngoài đề tài chính; năm ứng viên và A4 đã lưu trữ | [D-024](#d-024) |
| **Thiết kế đánh giá đề tài chính** | Mốc G2 là baseline thành phần trung thực **0,4897**, báo kèm trần nhãn **0,6514**; nhãn chính từ **bộ bão hòa**, bộ quét là nguồn phụ; nhãn trung bình hai replicate; split cụm protein **cov80**; 130 peptide hai nguồn cùng phía; không trộn BAG6 WT | [D-025](#d-025) |
| Thứ tự tiềm năng | Là **số đầu tên thư mục** trong `topics/` (ví dụ `1-ten-de-tai`), do Trọng tự đặt. **Chưa đặt** | [D-019](#d-019) |
| Định hướng chọn đề tài | 1) ưu tiên tin sinh học; 2) không bó vào dự đoán residue/peptide; 3) ưu tiên tầng công cụ/benchmark/nền tảng; 4) đề tài ngoài tin sinh học vẫn hợp lệ nhưng xếp sau. Mức 3 **đã được GVHD xác nhận là hợp lệ** | [D-017](#d-017), [D-022](#d-022) |
| Đóng góp dạng công cụ | **GVHD chấp nhận** (công cụ, thước đo, audit, benchmark, thuật toán tối ưu). Vẫn phải là đóng góp **dương** đo được | [D-022](#d-022), [D-012](#d-012) |
| Thước đo một ứng viên | 5 tiêu chí GVHD + 3 cổng bắt buộc G1/G2/G3, xem [course.md](project/course.md) | [D-006](#d-006), [D-012](#d-012) |
| Đã đóng (lưu trữ) | A2, A3, A4, dark kinome, budgeted PLM, metagenomic binning (D-024), RCA, RTK–ATP, TME senescence, cơ chất sirtuin, legal QA, quản lý chi tiêu, efflux, IL-6, sửa lỗi phần mềm. Xem [archive/](archive/README.md) | D-003, D-006, D-008, D-010, D-011, D-019, [D-021](#d-021) |
| Quy ước đang áp dụng | HTML để trong repo, không dùng artifact ([D-013](#d-013)). Repo private ([D-004](#d-004)) | — |

**Mốc tiếp theo:** **tuần 6 kết thúc 16/10/2026** (buổi gặp 1 là 02/10, tuần 4) — báo cáo lại đề tài với GVHD, trình `degron-footprint`. Buổi gặp **chưa định ngày**. Tài liệu trình bày **chưa cập nhật** theo yêu cầu của Trọng ngày 14/10, nên hiện chưa có bản khớp trạng thái hiện hành.

**Việc chặn gần nhất của đề tài chính:** **tính lực thống kê trên n = 91** — cỡ mẫu thật của bộ bão hòa sau ngưỡng peptide degron (PSI WT ≤ 3,0), không phải 235 ([pap-baseline §C](topics/degron-footprint/research/pap-baseline/README.md)). Đây là việc chặn **duy nhất** còn lại trước khi huấn luyện. Không có dự phòng ([D-026](#d-026)) nên điểm kiểm G2 cần đặt sớm, đề xuất cuối tuần 10. Không có dự phòng ([D-026](#d-026)), nên điểm kiểm G2 cần đặt sớm.

---

## C. Đề xuất chờ Trọng xác nhận

| # | Đề xuất | Người đề xuất | Ghi chú |
|---|---|---|---|
| C-7 | **Chuyển chỗ đặt đóng góp của `degron-footprint`: từ "kiến trúc mới" sang "benchmark mức residue đầu tiên + mô hình thắng trên nó"**, theo [lập luận lại 15/10](topics/degron-footprint/research/topic-argument-2026-10-15.md) §7. Lý do: [D-022](#d-022) đã cho phép đóng góp dạng công cụ; tính mới kiến trúc là chỗ yếu nhất (mọi cơ chế đều có tiền lệ, và cổng phơi lộ vừa mất vai trò — xem C-8); còn bộ trần nhãn + baseline + đối chứng ΔPAP + lực + split thì **đã đo xong** và không bài nào trong sáu bài đã đọc có | Claude, 15/10/2026 | **Cần Trọng quyết** vì đổi câu đóng góp của cả luận văn. Rủi ro phải nhận: [D-012](#d-012) vẫn đòi đóng góp **dương** đo được, nên mô hình vượt 0,4897 (hoặc AUROC vượt 0,7692) **vẫn bắt buộc**; benchmark một mình không đủ. GVHD từng nói kỳ vọng "kiến trúc chưa ai dùng" (11/10) nên nên hỏi lại cùng C-5 |
| C-8 | **Hạ cổng phơi lộ từ "điểm mới 1" xuống "cơ chế chuyển giao", và đưa nó ra khỏi đường găng của G2.** Lý do: toàn bộ nhãn huấn luyện chính là peptide 28-mer tách rời gắn đầu C của GFP, nên **mọi peptide phơi lộ như nhau** và rASA/pLDDT **không có phương sai** trên tập huấn luyện chính — tham số của cổng không nhận diện được. Xem [lập luận lại §4](topics/degron-footprint/research/topic-argument-2026-10-15.md). Thay lý lẽ kỹ thuật chính bằng **ngữ cảnh vị trí**, nơi có bằng chứng đo được (+0,1311 precision@3 khi đổi kernel 1 → 7, so với +0,0032 trên thang điểm khối) | Claude, 15/10/2026 | Đây là **lỗi lập luận trong thiết kế cũ**, không phải thay đổi sở thích — nhưng vẫn là đề xuất vì nó đổi thứ tự ưu tiên tám tuần còn lại. Phép đo 14/10 không mất giá trị, chỉ đổi vai sang phần chuyển giao |
| C-9 | **Đổi thước đo chính của ma trận từ Spearman sang AUROC mức ô**, vì trần nhãn Spearman chỉ 0,6989 còn trần AUROC đạt 0,9519 — xếp hạng mọi ô khó hơn hẳn việc tách ô dương khỏi ô âm, và nhiệm vụ của đề tài là cái sau. ΔPAP đạt 0,7692 nên dư địa **0,1827**, lớn hơn dư địa của bộ quét (0,1617) trên nhãn ít nhiễu hơn nhiều (16,7% so với 75,9%) | Claude, 15/10/2026 | Củng cố [D-025](#d-025) đề xuất 2 chứ không trái. Kèm điều kiện đã biết: cỡ mẫu thật là **91** peptide |
| C-10 | **Tải và dùng bộ nhân Larsen 2025 làm test chuyển assay/chuyển ngăn ở mức tile** — một file `annotations/transfac_tiles.csv.gz` 5,77 MB từ [repo GitHub giấy phép MIT](https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors), đã chú giải sẵn PAP/ADPred/rASA/pLDDT. Lợi ích: một mốc **PAP Pearson 0,79** do chính tác giả đo, cộng **chỗ duy nhất rASA/pLDDT có phương sai** (32% tile degron rASA > 0,7) nên là nơi kiểm được cổng phơi lộ ở mức tile, biến [C-8](#c-8) từ khẳng định thành số đo được. Chi phí: 5,77 MB + vài giờ. Xem [báo cáo 15/10 §2–4](topics/degron-footprint/research/larsen-nuclear-and-risks-2026-10-15/README.md) | Claude, 15/10/2026 | **Phải nói đúng tên:** đây là test **chuyển assay/chuyển ngăn**, **không** phải test trình tự chưa thấy — 97,4% TF của nó đã có trong peptidome GPS. Và nó **không đóng góp nhãn mức residue nào**, nên **không** phải đường thoát cho rủi ro nhãn residue. Kèm `data/raw/SOURCE.md` giữ thông báo MIT |
| C-11 | **Hai việc nhỏ về nguồn ngoài:** (a) gửi một email tới `rhpetersen@bio.ku.dk` xin xác nhận **giấy phép MIT trong repo phủ cả các file dữ liệu đầu ra**, không chỉ script (MIT nominally là giấy phép phần mềm, và Zenodo đăng ký loại "Software"); (b) quyết có **nhận [Degformer](lectures/degron-basics/papers/degformer-2026.md) làm baseline chính thức** trong luận văn hay không | Claude, 15/10/2026 | (a) rẻ và xoá sạch chỗ mơ hồ pháp lý duy nhất còn lại. (b) nếu nhận thì **phải trích rõ** "tự báo, chưa công bố, split ngẫu nhiên có 4,09% rò rỉ đo được", và con số 0,9162/0,9420 phải gọi là **Pearson**, không phải Spearman. ⚠ Checkpoint của nó là **pickle**, nạp nó thực thi mã tuỳ ý — xử lý như dữ liệu không tin cậy |
| C-5 | Xác nhận lại với GVHD ở tuần 6 rằng đóng góp dạng công cụ được nhận | Claude, 12/10/2026 | [D-022](#d-022) dựa trên thông tin Trọng truyền đạt, **chưa có biên bản**, và nó đọc lại lời GVHD ngày 11/10 theo hướng nhẹ hơn. Nên hỏi một câu xác nhận để khỏi phải đổi hướng muộn |

---

## B. Sổ quyết định (mới nhất ở trên)

Trường "Ai quyết": **Trọng** (sinh viên), **GVHD**, **Claude (ủy quyền)** — Trọng giao cho Claude tự quyết, **Claude (khuyến nghị)** — chỉ là khuyến nghị nhưng đã được dùng như quyết định.

### D-026
**14/10/2026 · Trọng · Hiệu lực.** **Chấp nhận không có đề tài dự phòng.** `degron-footprint` là đề tài duy nhất; các ứng viên đã lưu trữ ở D-024 không được giữ ở vai trò dự phòng. Hệ quả cần nhớ: nếu G2 không đạt thì không còn đường lui đã chuẩn bị, nên điểm kiểm G2 phải đặt sớm.

### D-025
**14/10/2026 · Trọng · Hiệu lực.** **Xác nhận toàn bộ bảy đề xuất C-6** từ [audit dữ liệu 13/10 §9](topics/degron-footprint/research/full-data-audit/README.md):
1. Mục tiêu G2 phát biểu theo baseline thành phần trung thực **0,4897** và báo kèm trần nhãn **0,6514**; bỏ cách nói "vượt 0,6045 / +28,9%" (0,6045 và 0,7792 là oracle đọc nhãn test).
2. **Bộ bão hòa là nguồn nhãn chính**, bộ quét là nguồn phụ và để mở rộng độ phủ. Điều kiện kèm: tính lại lực cho 235 peptide **trước khi** cam kết thiết kế.
3. Nhãn là trung bình hai replicate; mọi bảng kết quả báo kèm trần nhãn.
4. Split theo cụm protein **cov80**.
5. 130 peptide có cả hai nguồn nhãn nằm cùng phía train/test.
6. Nêu SVM của Zhang 2023 trong G3 và đề cương, làm rõ khác phạm vi peptide/residue.
7. Không trộn mẫu BAG6 WT với hai replicate kia.

### D-024
**14/10/2026 · Trọng · Hiệu lực.** **Lưu trữ mọi đề tài còn lại ngoài `degron-footprint`**: `plm-calibration-audit` (A4), `xai-fidelity-benchmark` (A2), `structure-sequence-leakage-audit` (A3), `dark-kinome-zero-shot`, `budgeted-plm-variant-scoring`, `scalable-metagenomic-binning` chuyển sang [archive/topics/](archive/README.md), giữ nguyên tài liệu, code và dữ liệu. Giải quyết đề xuất C-4. **Thay phần dự phòng của [D-023](#d-023)**: A4 không còn là dự phòng, hiện chưa có dự phòng; phần đề tài chính của D-023 giữ nguyên.

### D-023
**12/10/2026 · Trọng · Hiệu lực; phần dự phòng bị thay bởi [D-024](#d-024).** **Đề tài chính là [`degron-footprint`](topics/degron-footprint/README.md)** (dự đoán footprint / hiệu ứng đột biến degron mức residue trên nhãn thực nghiệm). **Dự phòng là [`plm-calibration-audit`](archive/topics/plm-calibration-audit/README.md)** (A4, công cụ audit calibration và miền áp dụng). Thay vị trí đề tài chính ở [D-021](#d-021) ("chưa có đề tài chính") và vị trí dự phòng ở [D-016](#d-016) (degron là dự phòng duy nhất); giải quyết đề xuất C-4 phần đề tài chính/dự phòng.

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
**10/10/2026 · Claude (khuyến nghị) · Bị thay bởi D-014.** Khuyến nghị dark kinome trên DARKIN làm đề tài chính. Loại sirtuin khỏi vị trí chính vì Trọng cho biết **GVHD không nhận kết quả âm làm đóng góp chính**. Ngày 11/10, sáu phép kiểm đã làm sụp trụ tính mới (xem [thẻ đề tài](archive/topics/dark-kinome-zero-shot/README.md)).

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
