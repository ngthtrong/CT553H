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
| **Thiết kế đánh giá đề tài chính** | **Ba nhãn, ba vai** ([D-031](#d-031)): **tile Voutsinos** cho chương đo lường cross-assay (4.308 cụm; trần **đo lường** 0,9778) · **bộ quét** cho **trục ngữ cảnh** của nhiệm vụ mức residue (2.994 peptide / **1.985 cụm** / 83.446 ô; trần đo lường AUROC **0,9458**) · **bộ bão hòa** cho **ma trận 19 thay thế** (91 peptide / **89 cụm** / 47.847 ô; trần **0,9519**). Thước đo chính **AUROC mức ô**, trung bình macro theo peptide, ghép cặp theo peptide, **bootstrap theo cụm**. Nhãn trung bình hai replicate; không trộn BAG6 WT | [D-031](#d-031), [D-028](#d-028) |
| **Việc của kiến trúc mới** | **Có mục tiêu bằng số** ([D-031](#d-031)): vượt **AUROC 0,7693** của ΔPAP `cnn2w1` trên ma trận bão hòa (trần đo lường 0,9519) — hiện mô hình của repo **thua 0,0420**. Sáu ứng viên đã loại bằng đo: trình tự/cụm chưa thấy, ngữ cảnh vị trí mức peptide, cổng phơi lộ, dịch chuyển assay, mô hình phi tuyến mạnh hơn, **vị trí tuyệt đối trong peptide** (+0,0002). Chỗ có tín hiệu là **lân cận cục bộ ±3** (+0,0289, trong đó 80% là *thành phần* của lân cận). Lý lẽ cho MIL **đã đổi**: không phải "chưa tìm thấy tiền lệ" mà **giám sát yếu từ nhãn mức túi** — chờ [C-17](#c-17) | [D-031](#d-031), [D-027](#d-027) |
| **Thứ tự tám tuần** | **Đang làm: chương mức residue (G2)** — huấn luyện trên ma trận bão hòa nhắm vượt 0,7693 · rồi bộ nhân Larsen → **điểm kiểm cứng tuần 10** → ứng dụng và viết. Chương cross-assay hạ xuống **chương đo lường**. **Tài liệu trình bày**: điều kiện của [D-030](#d-030) **đã đạt** (có hướng cụ thể + con số dương **+0,0300**), nhưng chỉ làm **khi Trọng yêu cầu** | [D-031](#d-031), [D-029](#d-029), [D-030](#d-030) |
| Thứ tự tiềm năng | Là **số đầu tên thư mục** trong `topics/` (ví dụ `1-ten-de-tai`), do Trọng tự đặt. **Chưa đặt** | [D-019](#d-019) |
| Định hướng chọn đề tài | 1) ưu tiên tin sinh học; 2) không bó vào dự đoán residue/peptide; 3) ưu tiên tầng công cụ/benchmark/nền tảng; 4) đề tài ngoài tin sinh học vẫn hợp lệ nhưng xếp sau. Mức 3 **đã được GVHD xác nhận là hợp lệ** | [D-017](#d-017), [D-022](#d-022) |
| Đóng góp dạng công cụ | **GVHD chấp nhận** (công cụ, thước đo, audit, benchmark, thuật toán tối ưu). Vẫn phải là đóng góp **dương** đo được. **Thêm 15/10:** dạng "đo và phân rã trần của một lớp bài toán" được nhận làm **khung**, nhưng **kiến trúc mới vẫn là thành phần bắt buộc** | [D-022](#d-022), [D-012](#d-012), [D-027](#d-027) |
| Thước đo một ứng viên | 5 tiêu chí GVHD + 3 cổng bắt buộc G1/G2/G3, xem [course.md](project/course.md) | [D-006](#d-006), [D-012](#d-012) |
| Đã đóng (lưu trữ) | A2, A3, A4, dark kinome, budgeted PLM, metagenomic binning (D-024), RCA, RTK–ATP, TME senescence, cơ chất sirtuin, legal QA, quản lý chi tiêu, efflux, IL-6, sửa lỗi phần mềm. Xem [archive/](archive/README.md) | D-003, D-006, D-008, D-010, D-011, D-019, [D-021](#d-021) |
| Quy ước đang áp dụng | HTML để trong repo, không dùng artifact ([D-013](#d-013)). Repo private ([D-004](#d-004)) | — |

**Mốc tiếp theo:** **tuần 6 kết thúc 16/10/2026** (buổi gặp 1 là 02/10, tuần 4). Buổi gặp **chưa định ngày**. Điều kiện của [D-030](#d-030) mục 1 (hướng đóng góp cụ thể + ít nhất một con số dương) **đã đạt 15/10 phiên 8**.

⚠ **Tài liệu trình bày — năm chỗ phải sửa, chưa sửa.** [`presentation/slide-content-2026-10-15.md`](topics/degron-footprint/presentation/slide-content-2026-10-15.md) (viết trong một phiên khác cùng ngày, trước khi phiên 8 đo xong) hiện **nói sai năm chỗ** so với trạng thái này. Claude **không tự sửa** theo dặn dò của Trọng; đây là danh sách để Trọng quyết khi nào sửa:

| Chỗ trong file slide | Đang nói | Phải thành |
|---|---|---|
| slide 17/20/22, "cam kết trước" | MDE ở n = 91 là **≈ 0,071** | **0,0123** — hụt **≈ 6 lần**; nếu trình bày nguyên trạng thì tự hạ thiết kế của mình |
| việc còn thiếu "đếm số cụm trong n = 91" | *chưa có* | **89 cụm** / 91 protein; và ICC ⇒ ≈ **1.416 ô độc lập hiệu dụng** |
| khung đề tài | *"C-15 chưa thành quyết định"* | **[D-031](#d-031)**, đã là quyết định của Trọng |
| tính mới kiến trúc | **MIL so với đầu theo vị trí**, *"chưa thấy ai báo cáo"* | lý lẽ này **yếu** — xem [C-17](#c-17); lý lẽ thay thế là **giám sát yếu từ nhãn mức túi** |
| bảng kết quả G2 | *chưa có con số dương* | **+0,0289 / +0,0300** trên bộ quét; **−0,0420** trên ma trận bão hòa (nói cả hai) |

Hai bản cũ hơn (`presentation.html`, `session-02-prep.md`, cả hai 11/10) vẫn gọi cổng phơi lộ là "Điểm mới 1" — điều [D-028](#d-028) mục 1 đã hạ.

**Việc chặn của đề tài chính: cả hai đã xử lý 15/10 (phiên 8)** — xem [báo cáo](topics/degron-footprint/research/residue-task-derisk-2026-10-15/README.md), quyết định [D-031](#d-031).

1. **Rủi ro "thành phần > vị trí"** ([LeBlanc 2026](lectures/degron-basics/papers/leblanc-2026.md)) — **thật trên nhãn mức peptide** (phiên 5: chỉ **28,9%** ô tách khỏi 0, đồng thuận dấu **0,684**, thành phần ổn định hơn ≈ **56×**), nhưng **khoanh được** trên nhãn **hiệu ứng đột biến**: 28,9% → **53,3%**, đồng thuận dấu → **0,90**, tỉ lệ áp đảo của thành phần **56× → 2,2×**. ⇒ Rủi ro còn, **không còn là việc chặn**.
2. **Lực trên n = 91** — **giải quyết.** 91 peptide nằm trên **91 protein / 89 cụm** cov80 (thư viện bão hòa chọn mỗi protein một peptide ⇒ lồng nhau mức protein gần như không có). Ghép cặp theo peptide + bootstrap theo cụm cho **MDE 0,0123** ở lực 80%, **không phải 0,071** — con số cũ suy từ phương sai *không ghép cặp*. Lực tại delta đo được: **0,995**. ICC ô-trong-peptide 0,0625 ⇒ **≈ 1.416 ô độc lập hiệu dụng**.

**Con số dương đầu tiên cho G2 (phiên 8) [đo]:** trên nhiệm vụ mức residue, **ngữ cảnh cục bộ ±3** đáng **+0,0289** AUROC so với lớp chỉ-thành-phần (CI [0,0264; 0,0313], 1.599 cụm) và **+0,0300** so với **ΔPAP `cnn2w7`** (CI [0,0234; 0,0366], 2.064 peptide / 1.471 cụm). ⚠ Phải nói kèm: ΔPAP **bị dùng ngoài mục đích**, và baseline chỉ-thành-phần **hoà** nó (+0,0008) ⇒ rào này **thấp**, chính vì chưa ai huấn luyện cho nhiệm vụ này.

**Phân rã delta — chỗ này đổi cách phát biểu đề tài:**

| Thành phần | Giá trị |
|---|---:|
| vị trí tuyệt đối trong peptide, một mình | +0,0052 |
| **thành phần cửa sổ ±3, không thứ tự** | **+0,0232** (80% của tổng) |
| thêm thứ tự trong cửa sổ | +0,0057 |
| thêm vị trí tuyệt đối lên trên ngữ cảnh | **+0,0002** ⇒ bằng 0 |

⇒ **Không** được nói "mô hình vị trí thắng mô hình thành phần". Câu đúng: *thành phần ở thang **lân cận ±3** thắng thành phần ở thang **cả peptide***. Cách này **tinh chỉnh** LeBlanc 2026 chứ không chống nó.

**Chỗ vẫn thua, và nay là mục tiêu G2 có số:** trên **ma trận bão hòa**, mô hình của repo (huấn luyện trên bộ quét, loại cụm trùng, chuyển sang 19 thay thế chưa thấy) đạt **0,7273** so với ΔPAP `cnn2w1` **0,7693** ⇒ **−0,0420** (CI [−0,0580; −0,0256]). Trần đo lường **0,9519**. Trên thang **mức vị trí** thì thứ tự **đảo** (0,4440 so với 0,3553) ⇒ phải báo theo từng thước đo.

Không có dự phòng ([D-026](#d-026)) nên điểm kiểm G2 cần đặt sớm — cuối tuần 10 ([D-028](#d-028) mục 3).

---

## C. Đề xuất chờ Trọng xác nhận

| # | Đề xuất | Người đề xuất | Ghi chú |
|---|---|---|---|
| <a id="c-16"></a>C-16 | **Dùng dữ liệu `CTNNB1` của Krishna 2026 làm đối chứng ngoài, độc lập.** *Nature Genetics* 58:366–375, DOI [10.1038/s41588-025-02496-5](https://doi.org/10.1038/s41588-025-02496-5): saturation genome editing tại locus nội sinh, **cả 342 đột biến missense** trên **codon 31–48** của degron β-catenin. Độc lập theo cả ba trục: nhóm tác giả khác, **assay khác**, **protein chưa thấy** (`P35222` **không** có trong bảng PSI của Zhang, **không** có trong thư viện TF của Larsen — đã kiểm). Và khớp đúng khuôn: codon 31–48 nằm **trọn** trong tile 2 của `P35222` (residue 24–51 theo quy tắc `(n−1)·23`) nên chấm được bằng đúng mô hình 28-mer hiện có. Giá trị: đóng rủi ro **cả hai nguồn nhãn mức residue đều của một nhóm tác giả (Zhang 2023)** | Claude, 15/10/2026 | ⚠ **Ba điều phải kiểm trước:** (a) readout là **tín hiệu Wnt**, không phải độ bền ⇒ chỉ gọi được là **đối chứng hội tụ**, không phải nhãn cùng loại; (b) **giấy phép chưa rõ** — bảng điểm từng biến thể nằm ở *Source data*/Supplementary, phần deposit công khai (GEO `GSE299075`, EGA `EGAS00001005364`) là RNA-seq chứ không phải điểm, code ở Zenodo mà [resources §4](resources/README.md) ghi **Zenodo trả 403 từ mạng này**; (c) **342 ô / 1 degron / 18 vị trí** ⇒ đủ làm đối chứng, **không** đủ huấn luyện. Chi tiết: [báo cáo §8](topics/degron-footprint/research/residue-task-derisk-2026-10-15/README.md) |
| <a id="c-17"></a>C-17 | **Đổi lý lẽ cho phần MIL của kiến trúc, và đổi luôn phát biểu "trục vị trí".** Hai sửa: (a) bỏ cách nói *"MIL so với đầu theo vị trí — chưa tìm thấy tiền lệ"*, vì tra y văn 15/10 cho thấy mô típ chuẩn là **đầu theo residue khi có nhãn mức residue, MIL khi chỉ có nhãn mức túi** ⇒ đặt MIL làm tính mới là **yếu**. Lý lẽ thay thế, có số đỡ: **giám sát yếu** — nhãn mức túi (GPS 260k peptide, tile 212k) **rất dồi dào nhưng không nhận diện được tham số vị trí** (28,9%), nhãn mức ô **nhận diện được nhưng ít** (89 cụm) ⇒ câu hỏi kiến trúc là *cầu nối MIL/attention có moi được thông tin mức residue từ nhãn mức túi hay không*, và **câu trả lời âm cũng dùng được**. (b) Mọi chỗ viết "vị trí thắng thành phần" sửa thành **"thành phần ở thang lân cận ±3 thắng thành phần ở thang cả peptide"** — theo phân rã +0,0232 / +0,0057 / +0,0002 | Claude, 15/10/2026 | Mục (b) là **sửa câu chữ bắt buộc** nếu [D-031](#d-031) có hiệu lực, vì nếu không thì đề tài phát biểu sai chính phép đo của mình. Mục (a) đổi **lý do**, không đổi việc phải làm |

**Đã giải quyết:** C-7 … C-14 ([D-027](#d-027), [D-028](#d-028)) và **C-15** ([D-031](#d-031)).

Còn lại **một việc phải làm, không phải việc phải quyết**:

| # | Việc | Trạng thái |
|---|---|---|
| C-11a | ✅ **Đã làm 15/10** — Trọng đã gửi email xin xác nhận MIT phủ cả file dữ liệu đầu ra ([D-030](#d-030) mục 2). **Đang chờ trả lời** | **Đang chờ** |
| C-5 | **Hỏi GVHD xác nhận** ở buổi gặp: đóng góp có khung "đo và phân rã trần của một lớp bài toán" **kèm một kiến trúc mới** thì có đạt kỳ vọng không? Cùng đó xác nhận lại [D-022](#d-022) (đóng góp dạng công cụ) vì nó dựa trên thông tin Trọng truyền đạt, **chưa có biên bản** | **Chưa làm.** Buổi gặp chưa định ngày. [D-027](#d-027) là quyết định của **Trọng**, không phải của GVHD |

---

## B. Sổ quyết định (mới nhất ở trên)

Trường "Ai quyết": **Trọng** (sinh viên), **GVHD**, **Claude (ủy quyền)** — Trọng giao cho Claude tự quyết, **Claude (khuyến nghị)** — chỉ là khuyến nghị nhưng đã được dùng như quyết định.

### D-031
**15/10/2026 (phiên 8) · Trọng · Hiệu lực.** **Chấp nhận C-15 ([nguyên văn đề xuất](topics/degron-footprint/research/cross-assay-model-2026-10-15/README.md)): nhiệm vụ mức residue là trụ đóng góp; phần cross-assay hạ xuống một chương đo lường.** Trọng ra lệnh *"tiến hành thực hiện đề xuất C-15, nghiên cứu thêm để giảm thiểu rủi ro và trình bày được đóng góp rõ ràng"*. Báo cáo thực hiện: [residue-task-derisk-2026-10-15](topics/degron-footprint/research/residue-task-derisk-2026-10-15/README.md).

Năm hệ quả **đã đo xong trong cùng phiên**, nên quyết định này không còn kèm rủi ro mở như C-15 đã ghi:

1. **Hai việc chặn đóng lại.** Lực trên n = 91: **MDE 0,0123** ở lực 80% (ghép cặp theo peptide, bootstrap theo **89 cụm**), không phải 0,071 — con số cũ suy từ phương sai *không ghép cặp*. Rủi ro LeBlanc: **khoanh được**, tỉ lệ áp đảo của thành phần giảm từ ≈ **56×** (nhãn mức peptide) xuống **2,2×** (nhãn hiệu ứng đột biến), % hệ số ngữ cảnh tách khỏi 0 tăng **28,9% → 53,3%**.

2. **Thiết kế đánh giá thành ba nhãn ba vai, sửa [D-028](#d-028) mục 5.** Phát biểu "bộ bão hòa là nguồn **duy nhất** đỡ được mức residue" **không chính xác**: **bộ quét** cũng là nhãn hiệu ứng đột biến, và lớn hơn nhiều (**2.994 peptide / 1.985 cụm / 83.446 ô** so với 91 / 89 / 47.847). Vai đúng: bộ quét đỡ **trục ngữ cảnh**, bộ bão hòa đỡ **ma trận 19 thay thế**. ⇒ Câu "n = 91 là cỡ mẫu của phần mức residue" **phải bỏ**.

3. **Con số dương cho G2 đã có:** ngữ cảnh cục bộ ±3 đáng **+0,0289** AUROC so với lớp chỉ-thành-phần và **+0,0300** so với ΔPAP `cnn2w7`. ⇒ Điều kiện của [D-030](#d-030) mục 1 **đã đạt**. Nhưng tài liệu trình bày **vẫn chỉ làm khi Trọng yêu cầu**.

4. **Việc của kiến trúc đổi từ một câu sang một con số:** vượt **0,7693** AUROC mức ô của ΔPAP `cnn2w1` trên ma trận bão hòa (hiện thua **0,0420**), trần đo lường 0,9519, ngưỡng phát hiện **0,0123** đã tính trước. Ứng viên **"vị trí tuyệt đối trong peptide"** bị **loại** (+0,0002) — ứng viên thứ sáu bị loại bằng đo.

5. **Hai sửa câu chữ bắt buộc đi kèm**, ghi thành [C-17](#c-17): không nói "vị trí thắng thành phần" (phải nói **thang lân cận ±3** thắng **thang cả peptide**), và đổi lý lẽ cho MIL sang **giám sát yếu từ nhãn mức túi**.

**Ba chỗ câu chữ mà C-15 yêu cầu sửa đã xử lý:** (a) và (b) — mục A không còn con số **+0,1061** lẫn cụm "dư địa đến trần"; mọi trần nay gọi là **trần đo lường**. (c) nhánh stacking đã ghi là vô nghĩa do cộng tuyến ở [báo cáo cross-assay §3.1](topics/degron-footprint/research/cross-assay-model-2026-10-15/README.md). Các báo cáo phiên 3–4 **giữ nguyên làm lịch sử**, có ghi chú đính chính ở đầu.

### D-030
**15/10/2026 · Trọng · Hiệu lực.** Ba việc.

1. **Chưa làm tài liệu trình bày với GVHD khi chưa chốt được hướng đi cụ thể về đóng góp.** **Thay mục tuần 6–7 của [D-029](#d-029)**: việc tài liệu **lùi lại** cho tới khi có một **hướng đóng góp cụ thể** — nghĩa là một đề xuất kiến trúc rõ ràng **kèm ít nhất một con số dương** trên nhiệm vụ cross-assay. Hệ quả: phần việc **mô hình cross-assay + kiến trúc** (vốn ở tuần 7–8) **lên trước**, và trở thành việc đang làm. Phần còn lại của D-029 (Larsen → chương residue → điểm kiểm tuần 10 → ứng dụng và viết) giữ nguyên thứ tự tương đối.

   Lý do Trọng nêu: trình bày một khung đóng góp chưa có hướng cụ thể thì không dùng được trong buổi gặp. Điều này **đảo** đánh đổi mà D-029 đã chọn (ưu tiên duyệt đề tài trước G2) — và nhận lại rủi ro ngược: GVHD vẫn chưa duyệt đề tài nào trong lúc tám tuần đang chạy.

2. **[C-11a](#c-11a) đã thực hiện** — Trọng **đã gửi email** xin xác nhận giấy phép MIT phủ cả file dữ liệu đầu ra. Đang **chờ trả lời**; cho tới khi có trả lời thì chỗ mơ hồ pháp lý vẫn ghi nguyên trong [SOURCE.md](topics/degron-footprint/data/raw/larsen-2025/SOURCE.md).

3. **`SOURCE.md` được lên git.** Đổi quy ước: **hai** loại file trong `data/` lên git, không còn một — `data/README.md` và `SOURCE.md` ở mọi độ sâu, để **thông báo giấy phép nguyên văn** đi theo repo. Đã sửa `.gitignore` và [CLAUDE.md](CLAUDE.md).

   ⚠ **Ghi lại một lỗi đã mắc và đã sửa trong cùng phiên:** bản sửa `.gitignore` đầu tiên của Claude (`!**/data/**/`) **mở chặn toàn bộ ~1,9 GB dữ liệu**, và bản thứ hai khiến nested git repo `voutsinos-2026/repo/` bị thêm thành **gitlink**. Bản cuối dùng `**/data/**` + `!**/data/raw/` + `!**/data/raw/*/` + `!**/data/**/SOURCE.md`, đã kiểm bằng `git check-ignore` và `git add -An` trên cả `topics/` và `archive/`: **chỉ** `data/README.md` và `SOURCE.md` được thêm. Lần sau đổi `.gitignore` của `data/` thì **bắt buộc** chạy `git add -An` trước khi coi là xong.

### D-029
**15/10/2026 · Claude (ủy quyền: Trọng "em tự xếp thứ tự") · Hiệu lực; mục tuần 6–7 bị thay bởi [D-030](#d-030).** **Thứ tự tám tuần còn lại.** Căn cứ: rủi ro lớn nhất không phải kỹ thuật mà là **chưa đề tài nào được GVHD duyệt** sau khi năm phiên đo 15/10 đã đổi mốc cam kết, nhãn chính và định nghĩa việc-của-kiến-trúc; và G2 là cổng **duy nhất** chưa đạt.

| Tuần | Việc | Ghi chú |
|---|---|---|
| **6–7** | **Tài liệu trình bày khớp trạng thái + ba câu hỏi cho GVHD** ([C-5](#c-5), và xác nhận [D-027](#d-027)) | ⚠ **Chờ Trọng bật đèn xanh**: Trọng đã dặn không tự sửa `presentation/` khi chưa được yêu cầu |
| **7–8** | **Mô hình cross-assay đầu tiên + thành phần kiến trúc mới** — nhắm vượt Spearman **0,7786** (trần 0,9778) | Đây là lần thử G2 thật đầu tiên. Kiến trúc nhắm **dịch chuyển định dạng assay** theo [D-027](#d-027) |
| **8** | **[C-10](#c-10): tải bộ nhân Larsen → mức 5 của bậc thang** (chuyển ngăn tế bào) | Rẻ (5,77 MB), mở rộng phần phân rã |
| **9** | **Chương mức residue**: tính lực trên n = 91 rồi mô hình residue | Nhãn đột biến là nguồn **duy nhất** đỡ được mức residue ([D-028](#d-028) mục 5) |
| **10** | **Điểm kiểm cứng** theo [C-12](#c-12) | Nếu chưa có con số vượt baseline thì chuyển trọng tâm sang benchmark + ứng dụng |
| **11–13** | **Ứng dụng** (API, ma trận 28×20, bất định neo vào trần nhãn, cờ ngăn tế bào) và **viết** | Bốn tính năng đã kiểm là chỗ khác biệt duy nhất với năm tiền lệ |

**Hai việc ngoài bảng, làm sớm khi tiện:** [C-11a](#c-11a) soạn email xin xác nhận giấy phép MIT — **Claude soạn nháp, Trọng đọc và tự gửi**, không tự gửi thay; và các việc câu chữ rẻ ở [C-12](#c-12).

**Điều thứ tự này nhận rủi ro:** đặt tuần 6–7 vào tài liệu nghĩa là **hoãn G2 thêm một tuần** trong khi không có dự phòng ([D-026](#d-026)). Đánh đổi có ý thức: tám tuần đặt trên một cách đóng góp GVHD chưa duyệt thì rủi ro hơn.

### D-028
**15/10/2026 · Trọng · Hiệu lực.** **Chấp nhận cả tám đề xuất đang chờ.** Phần C nay chỉ còn [C-5](#c-5) (một việc phải làm, không phải việc phải quyết).

1. **[C-8](#c-8)** — cổng phơi lộ hạ xuống **cơ chế chuyển giao**, ra khỏi đường găng G2.
2. **[C-9](#c-9)** — thước đo chính của ma trận là **AUROC mức ô** (trần 0,9519), không phải Spearman (trần 0,6989).
3. **[C-12](#c-12)** — có **hai** việc chặn, không phải một; kiểm ổn định seed/bootstrap lên trước huấn luyện (**đã chạy 15/10, rủi ro là thật**); **điểm kiểm cứng cuối tuần 10**.
4. **[C-14](#c-14)** — **giữ** split cụm cov80 nhưng **thôi coi là điểm thiết kế chính**; chuyển ngân sách lập luận sang **split theo assay**.
5. **[C-13](#c-13) bản đã sửa** — **tile Voutsinos là nhãn chính của phần benchmark và phân rã**; **bộ bão hòa giữ vai duy nhất cho mọi tuyên bố mức residue**. Hai nguồn **không thay thế nhau**. **Sửa một phần [D-025](#d-025) đề xuất 2.** Việc chặn "lực trên n = 91" **không mất**, thu hẹp vào chương mức residue.
6. **[C-10](#c-10)** — tải bộ nhân Larsen 2025 (5,77 MB, MIT qua GitHub) làm **mức 5 của bậc thang** (chuyển assay/chuyển ngăn mức tile), kèm `data/raw/SOURCE.md`.
7. **[C-11a](#c-11a)** — gửi email xin xác nhận MIT phủ cả file dữ liệu đầu ra.
8. **[C-11b](#c-11b)** — **nhận Degformer làm baseline chính thức**, với điều kiện trích rõ *"tự báo, chưa công bố, split ngẫu nhiên có 4,09% rò rỉ đo được"* và gọi 0,9162/0,9420 là **Pearson**. ⚠ Checkpoint là **pickle** ⇒ nạp nó thực thi mã tuỳ ý: thư mục riêng, `python3 -I`.

**[C-7](#c-7) đóng** — đã được [D-027](#d-027) giải quyết theo hướng thuận có điều kiện (nhận khung "đo và phân rã", giữ yêu cầu kiến trúc mới).

### D-027
**15/10/2026 (tối) · Trọng · Hiệu lực.** **Đóng góp dạng "đo và phân rã trần của một lớp bài toán" được nhận, nhưng đề tài **vẫn nên có kiến trúc mới**.** Giải quyết [C-7](#c-7) theo hướng **thuận có điều kiện** (không phải thay thế): mạch "benchmark + phân rã" được dùng làm **khung** của đóng góp, còn tính mới kiến trúc **vẫn là một thành phần bắt buộc**, không được bỏ. Hệ quả: cách đặt đóng góp ở [lập luận lại §7.1](topics/degron-footprint/research/topic-argument-2026-10-15.md) được nhận, nhưng **không** được dừng ở đó.

Hệ quả cho [C-13](#c-13): mạch H1 (phân rã khoảng cách qua assay) được giữ, và **phép đo ngày 15/10 vừa định nghĩa xong nhiệm vụ cho kiến trúc mới** — xem [báo cáo đo khoảng cách qua assay](topics/degron-footprint/research/reframe-options-2026-10-15/README.md) §9: khoảng cách qua assay là **0,0773 AUROC** (trần trong assay 0,9813 → qua assay 0,9041) và **gần như toàn bộ là hệ thống, không phải nhiễu** (hai assay đều rất tin cậy: 0,9749 và 0,9807; tương quan thật sau chỉnh suy giảm chỉ **0,7854**). Trên **dải khó** 2,0 < PSI < 4,0 thì AUROC qua assay rơi xuống **0,7839** và |r| xuống **0,5291**. ⇒ **Việc của kiến trúc mới là xử lý dịch chuyển định dạng assay, và phải được chấm trên dải khó**, không phải trên toàn dải.

Provenance đã xác nhận 15/10: **quyết định của chính Trọng**, không phải lời GVHD truyền đạt. Vì vậy [C-5](#c-5) **vẫn mở** — vẫn cần hỏi GVHD xác nhận ở buổi gặp, và câu hỏi nay gọn hơn: *đóng góp có khung "đo và phân rã" kèm một kiến trúc mới thì có đạt kỳ vọng không?*

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
