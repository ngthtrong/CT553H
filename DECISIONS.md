# Quyết định của dự án — nơi duy nhất

> **Nguồn quyết định duy nhất.** Trạng thái hiện hành nằm ở A; hiệu lực từng khoản nằm ở B. Tài liệu khác dẫn link tới đây, không tự ghi quyết định. Các khối **nguyên văn lịch sử** giữ câu chữ tại thời điểm ghi, không dùng làm kế hoạch hiện tại.
>
> **Cách đọc:** [A. Hiện hành](#hien-hanh) → [C. Chờ xác nhận](#cho-xac-nhan) → [D. Theo dõi](#theo-doi); tra [B1. Nghiên cứu degron](#nghien-cuu-degron) hoặc [B2. Quy ước repo](#quy-uoc-repo) khi cần căn cứ. [B3. Lịch sử](#lich-su) được thu gọn.
>
> **Cách cập nhật:** A chỉ sửa đè, tối đa khoảng một màn hình; không cộng dồn báo cáo đo. B giữ nguyên mã, không xoá quyết định; thêm mã kế tiếp vào đầu nhóm B1/B2 phù hợp và chỉ rõ khoản bị thay. C chỉ chứa lựa chọn chưa được xác nhận. D theo dõi việc thực hiện hoặc phản hồi bên ngoài; hoàn thành việc không đồng nghĩa hết hiệu lực quyết định. Quy ước đầy đủ: [CLAUDE.md](CLAUDE.md).

<a id="hien-hanh"></a>
<a id="a-hiện-hành--cập-nhật-14102026"></a>
<a id="a-hiện-hành--cập-nhật-15102026"></a>

## A. Trạng thái hiện hành

*Cập nhật 15/10/2026. Mốc học phần gần nhất: tuần 6 kết thúc 16/10. **Buổi gặp GVHD: 16/10/2026** (Trọng xác nhận ngày 15/10) — xem [C-5](#c-5).*

| Mục                      | Hiện hành                                                                                                                                                                                             | Căn cứ                                                                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Đề tài / phê duyệt   | **`degron-footprint`**, không có dự phòng; **chưa được GVHD duyệt**                                                                                                              | [D-023](#d-023), [D-026](#d-026), [C-5](#c-5)                                                                                                           |
| Trụ đóng góp          | Footprint / hiệu ứng đột biến **mức residue**; cross-assay là chương đo lường. **Thêm 15/10:** trụ **cấp thiết** (tỉ số chênh gây bệnh/lành tính **2,148** trong vùng degron) và trụ **phần mềm** (dịch vụ dự đoán có bất định + harness đánh giá)                                                        | [D-031](#d-031), [D-033](#d-033)                                                                                                                      |
| Cấp thiết (đo được)   | **Ở mức VÙNG:** degron giàu biến thể gây bệnh **2,148×** so với lành tính (MH theo protein, 3.114 tầng); **530.412 VUS** trong vùng degron. ⚠ **Ở mức RESIDUE: chưa thiết lập được** — ba phép đo đều nhất quán với rỗng (tầng có lực nhất: AUC **0,5166** [0,479; 0,554]) ⇒ **cấm** nói "residue đề tài dự đoán là residue mang tín hiệu bệnh"; ClinVar **không** dùng làm đích xác nhận. Còn phải nói kèm: **không** giàu lên theo *vị trí*; chưa khử bảo tồn/vô trật tự | [D-036](#d-036), [D-033](#d-033), [báo cáo](topics/degron-footprint/research/variant-coverage-2026-10-15/README.md) |
| Phạm vi               | **Degron tự trị**, biến thể **dòng mầm** — **đã chốt**. Degron có điều kiện (7/8 degron lái ung thư kinh điển) **ngoài tầm assay** — đã đo, không phải giả định. Không dùng "đột biến lái ung thư" làm mạch dẫn | [D-035](#d-035), [D-033](#d-033)                                                                                                                      |
| Tiến độ                | Đã huấn luyện ridge, có bằng chứng dương trên bộ quét; **G2 chưa hoàn tất**. Chưa huấn luyện mô hình sâu, chưa huấn luyện trên ma trận bão hòa; chưa xây ứng dụng | [Báo cáo phiên 8](topics/degron-footprint/research/residue-task-derisk-2026-10-15/README.md), [README đề tài](topics/degron-footprint/README.md) |
| Việc G2 tiếp theo       | Học ma trận bão hòa; mốc ΔPAP hiện tại **AUROC 0,7693**. **Degformer vẫn là baseline chính thức** phải đối chứng                                                            | [D-031](#d-031), [D-028](#d-028)                                                                                                                       |
| Đánh giá               | Bộ quét: ngữ cảnh; bão hòa: 19 thay thế; tile: đo lường cross-assay. AUROC mức ô, macro theo peptide; ghép cặp theo peptide, bootstrap theo cụm, split cov80                             | [D-031](#d-031), [D-025](#d-025), [D-028](#d-028)                                                                                                       |
| Yêu cầu đóng góp     | Đóng góp dương + thành phần kiến trúc mới + ứng dụng; khung đo và phân rã đã được **Trọng** nhận. **Mới 15/10: GVHD xác nhận trụ phần mềm** (dịch vụ dự đoán có bất định + harness) **được tính là đóng góp** — chưa có biên bản, xin ghi biên bản ở buổi gặp 16/10. Không nới cổng G2 và không bỏ yêu cầu kiến trúc mới | [D-034](#d-034), [D-006](#d-006), [D-012](#d-012), [D-027](#d-027), [C-5](#c-5)                                                                           |
| Thứ tự / mốc kiểm tra | Residue G2 → đánh giá trên bộ nhân Larsen đã tải → **cuối tuần 10** → ứng dụng và viết; tài liệu trình bày theo yêu cầu của Trọng                                       | [D-031](#d-031), [D-029](#d-029), [D-030](#d-030)                                                                                                       |
| Đang chờ / tài liệu   | **Hàng đợi C đã trống** — C-16…C-19 giải quyết bởi [D-035](#d-035). Còn chờ **bên ngoài**: [C-5](#c-5) (GVHD duyệt khung, **buổi gặp 16/10**) và [C-11a](#c-11a) (email giấy phép). Nội dung slide **đã cập nhật theo D-033…D-036** (26 slide, thêm phần Product; phiên 11), **chưa dựng slide**; câu hỏi 1 và 4 của slide cuối **chờ Trọng viết** | [Theo dõi](#theo-doi), [slide-content](topics/degron-footprint/presentation/slide-content-2026-10-15.md)                                              |

<a id="so-quyet-dinh"></a>

## B. Sổ quyết định

**Ba thông tin tách biệt:** hiệu lực (`Còn áp dụng` / `Một phần` / `Bị thay`), phạm vi (`Nghiên cứu` / `Repo` / `Lịch sử, bối cảnh`) và tiến độ thực hiện (ở [D](#theo-doi) hoặc README/log đề tài). Đưa vào lịch sử không tự bãi bỏ một quyết định đóng đề tài hay một điều kiện hợp lệ.

**Người quyết:** Trọng; GVHD (ghi rõ biên bản hay Trọng truyền đạt); Claude (ủy quyền, kèm lời giao quyền); Claude (khuyến nghị, được dùng làm chuẩn từ trước). Không đổi nguồn thẩm quyền của hồ sơ cũ khi biên tập. Quyết định mới nhất: [D-036](#d-036).

<a id="nghien-cuu-degron"></a>

### B1. Còn chi phối nghiên cứu degron

Trong từng nhóm, mã mới nhất ở trên. Phần **còn áp dụng / đã bị thay** là bản đọc hiện hành; mở nguyên văn khi cần truy vết. Số liệu và diễn giải chi tiết dẫn về báo cáo, không chép lại vào A.

<a id="d-036"></a>

#### D-036 — Trụ 1 giữ ở mức vùng; mắt nối tới mức residue chưa thiết lập được

**15/10/2026 (phiên 10, cuối) · Claude (ủy quyền) · Còn áp dụng.** Đây là **giới hạn do phép đo áp đặt**, không phải một lựa chọn: ba phép đo độc lập đều nhất quán với rỗng. Ghi dưới cùng ủy quyền của [D-035](#d-035) vì nó quyết định **đề tài được phát biểu điều gì**. Báo cáo: [variant-coverage §8b](topics/degron-footprint/research/variant-coverage-2026-10-15/README.md).

- **Điều đã đo.** Câu hỏi: ở độ phân giải **residue**, biến thể gây bệnh có nằm ở ô bị phá degron mạnh hơn biến thể lành tính không? (1) Nhị phân footprint/không: **OR 0,777** [0,530; 1,139]. (2) ΔPSI liên tục, khớp **vị trí**, tầng **có lực nhất** (n = 1.624, 620 cụm): **AUC 0,5166** [0,479; 0,554]. (3) ΔPSI liên tục, khớp **đúng ô**, nhãn sạch nhất nhưng n = 51: AUC 0,6738 [0,489; **0,831**] — CI **vẫn chạm 0,5**. Ghép cặp trong cùng peptide: hiệu +0,033 [−0,079; +0,141], 51,2% peptide dương.
- **Phát biểu được và không được phát biểu.** ✅ *“Vùng degron giàu biến thể gây bệnh 2,148 lần”* ([D-033](#d-033)) — **giữ nguyên, không bị phép đo này ảnh hưởng**, vì nó là tuyên bố mức **vùng**. ❌ *“Residue mà đề tài dự đoán là residue mang tín hiệu bệnh”* — **cấm**, đã đo ba lần và chưa thấy. ❌ **Không dùng ClinVar làm đích xác nhận mô hình**; ClinVar chỉ là **động lực** (530.412 VUS chưa ai gán cơ chế).
- **Mắt nối này không đóng được bằng dữ liệu hiện có.** Bộ bão hòa chỉ 91 peptide ⇒ số biến thể khớp đúng ô bị chặn ở **≈51 ca có phân loại**. Tăng lực cần **nguồn nhãn mức residue mới**, trùng với lỗ mà [D-035](#d-035) để lại khi bỏ đối chứng `CTNNB1`. Hai việc này nay là **một** việc.
- **Mạch đáng theo nhưng chưa đủ đỡ, ghi để không quên:** hiệu ứng **tăng đơn điệu** khi khớp chặt hơn và nhãn sạch hơn (0,517 → 0,520 → 0,674; trung vị ΔPSI gây bệnh **gấp 4,6 lần** lành tính ở tầng sạch nhất). Đúng dạng của một hiệu ứng thật bị nhiễu nhãn làm suy giảm — nhưng n = 51 **không chở được** một tuyên bố. Không được trích con số 0,674 rời khỏi CI của nó.
- **Không đổi:** G2, yêu cầu kiến trúc mới, ba trụ của khung. Đề tài **không cần** mắt nối này để hợp lệ — nó được đánh giá bằng nhãn thực nghiệm của chính nó. Điều D-036 ngăn là **tuyên bố quá tầm**.

<a id="d-035"></a>

#### D-035 — Giải quyết C-16, C-17, C-18, C-19 (ủy quyền)

**15/10/2026 (phiên 10) · Claude (ủy quyền) · Còn áp dụng.** Lời giao quyền của Trọng: *“bạn được ủy quyền trong phiên này để xác nhận các c như c-18 c-19 c-17 c-16,… miễng là đổi khung đề tài và đóng góp có ý nghĩa hơn”*. Phạm vi ủy quyền: **chỉ trong phiên này**, và chỉ cho các mục C về **khung đề tài và đóng góp**.

- **[C-18](#c-18) — nhận.** Phạm vi là **degron tự trị** và biến thể **dòng mầm**. Bỏ mọi cách nói “đột biến lái ung thư” khỏi mạch dẫn nhập. Lý do đạt điều kiện “có ý nghĩa hơn”: nó **gỡ một tuyên bố sẽ sụp khi bị hỏi** (7/8 degron lái ung thư kinh điển không hiện ra trong assay — đã đo) và **thay bằng một tuyên bố có số đỡ** (tỉ số chênh 2,148). Đổi **ví dụ dẫn**, không đổi con số.
- **[C-17](#c-17) — nhận cả (a) và (b).** (b) là sửa câu chữ bắt buộc, đã áp dụng trong nội dung slide: *“thành phần ở thang lân cận ±3 thắng thành phần ở thang cả peptide”*. (a) đổi lý lẽ MIL sang **giám sát yếu từ nhãn mức túi**, và **bỏ** cách nói “chưa tìm thấy tiền lệ” làm căn cứ tính mới. ⚠ Nhận (a) **không** đồng nghĩa duyệt một thiết kế MIL cụ thể — cảnh báo của [D-032](#d-032) giữ nguyên; thiết kế vẫn phải qua ablation.
- **[C-19](#c-19) — nhận: [C-16](#c-16) chuyển sang *không dùng*.** Căn cứ là bằng chứng đo được, **không** phải vấn đề giấy phép: tile 24–51 của `P35222` (chứa trọn codon 31–48) **có trong peptidome GPS, đo tốt** (reads 145/66) và **PSI 5,27 / 5,36** ⇒ không phải degron. Một đối chứng trên tile đó sẽ cho kết quả âm **vì lý do assay**, không phân biệt được với “mô hình sai”.
- **Giá phải trả của C-19, nói thẳng:** rủi ro *“cả hai nguồn nhãn mức residue đều của một nhóm tác giả (Zhang 2023)”* **vẫn mở và nay không có ứng viên nào**. Đây là chỗ C-19 **làm yếu đi** chứ không mạnh lên; nhận nó vì xây trên một đối chứng đã biết là hỏng thì tệ hơn. Yêu cầu cho ứng viên thay thế, ghi để tìm sau: readout phải là **độ bền** (không phải tín hiệu Wnt hay hoạt tính), trên **degron tự trị**, từ **nhóm tác giả khác**, và có nhãn **mức residue**. Chưa tìm thấy; rủi ro này phải nằm trong phần giới hạn của đề cương.
- **Không thuộc phạm vi ủy quyền này, giữ nguyên trạng:** [C-5](#c-5) (phải do GVHD trả lời, buổi gặp 16/10) và [C-11a](#c-11a) (chờ email bên ngoài trả lời). Claude **không** tự đóng hai mục đó.

<a id="d-034"></a>

#### D-034 — GVHD xác nhận trụ phần mềm được tính là đóng góp

**15/10/2026 · GVHD (Trọng trao đổi trực tiếp, Trọng truyền đạt) · Còn áp dụng.** Trọng cho biết đã trao đổi trực tiếp với GVHD và được xác nhận: **trụ phần mềm — dịch vụ dự đoán có bất định và harness đánh giá — được tính là đóng góp**. Nguyên liệu thô ghi ở [people.md](project/people.md).

- **Hệ quả:** trụ phần mềm của [D-033](#d-033) không còn là suy đoán về kỳ vọng của GVHD; nó là một đóng góp **đã được chấp nhận về nguyên tắc**. Củng cố [D-022](#d-022) (đóng góp dạng công cụ) bằng một lời xác nhận mới hơn và cụ thể hơn.
- **Không nới cổng nào.** Vẫn phải có **đóng góp dương đo được** ([D-012](#d-012)) — G2 chưa đạt, mục tiêu vượt **0,7693** không đổi. Vẫn phải có **thành phần kiến trúc mới** ([D-027](#d-027)); lời 11/10 của GVHD (“kỳ vọng một kiến trúc chưa ai dùng”) **được giữ**, không bị lời này thay. Tiêu chí 5 vẫn không thể thiếu ([D-006](#d-006)).
- ⚠ **Vẫn chưa có biên bản.** Đây là thông tin Trọng truyền đạt, như lời 12/10 ở [D-022](#d-022). Buổi gặp **16/10/2026** là chỗ xin duyệt **khung đề tài**, nên [C-5](#c-5) **vẫn mở** và nay gọn hơn: xin duyệt khung gồm **ba trụ** (cấp thiết đo được · phương pháp kèm kiến trúc mới · phần mềm), và xin **ghi biên bản** cho lời xác nhận này.

<a id="d-033"></a>

#### D-033 — Lập luận cấp thiết đo được, và tầng phần mềm thành thành phần đóng góp

**15/10/2026 (phiên 10) · Trọng · Còn áp dụng.** Trọng yêu cầu: *“chạy phép kiểm độ phủ trước, nếu khả quan tiến hành cập nhật lại topics degron này theo hướng bạn vừa đề xuất, nhớ cập nhật luon thông tin về phần mềm vào quyết định”*. Điều kiện **“khả quan” đã đạt** theo ngưỡng cam kết trước khi chạy (*vài trăm biến thể chấm được thì lập luận đứng; vài chục thì không*): số chấm được bằng **đúng ô thực nghiệm** là **≈ 1.600** (575 bão hòa + 1.037 quét), trong đó ≈ 1.350 là VUS. Báo cáo: [variant-coverage-2026-10-15](topics/degron-footprint/research/variant-coverage-2026-10-15/README.md).

- **Trụ cấp thiết nay là một con số, không phải một khẳng định.** Vùng protein mà thực nghiệm đo được là degron giàu biến thể **gây bệnh** so với **lành tính** gấp **2,148 lần** (CI 95% [2,072; 2,227]), Mantel–Haenszel phân tầng **theo protein**, 3.114 tầng có thông tin; theo cụm cov80 là 2,094 [2,024; 2,167]. Khử nhiễu mức gene theo thiết kế, nên không phải tạo tác của việc ClinVar dồn vào gene bệnh. Đây là lập luận “vì sao đáng làm” đầu tiên của đề tài dựa trên số đo, và nó lấp chỗ hở mà [đánh giá trung thực §4](topics/degron-footprint/research/contribution-assessment-2026-10-15.md) đã nêu.
- **Tầng phần mềm là một thành phần đóng góp, không phải vỏ ngoài.** Hai phần, theo thứ tự Trọng đã chọn: (a) **trụ** — dịch vụ dự đoán có **bất định neo vào trần đo lường**, API, chấm đột biến tuỳ ý, cờ ngăn tế bào, xuất xứ nhãn; (b) **chương đánh giá** — harness tái lập nạp các tiền lệ, áp cùng split cụm cov80, báo delta kèm trần đo lường và MDE. Lý do phần mềm đứng được ở đây chứ không phải ở chỗ khác: nút cổ chai của bài toán **không** phải độ chính xác — 75,9% dư sau oracle thành phần là nhiễu đo, trần đo lường 0,9458/0,9519 ([full-data-audit](topics/degron-footprint/research/full-data-audit/README.md)).
- **Miền áp dụng mở rộng sang peptidome GPS.** 116.702 tile degron trên 17.287 protein (ngưỡng PSI ≤ 3,0), trong đó **87,3% cụm cov80 chưa thấy** trong tập huấn luyện và 67,9% tile nằm trên protein chưa thấy. Repo đã có file này từ 13/10 nhưng chưa dùng làm miền áp dụng. Hệ quả: mọi tuyên bố tổng quát hóa vẫn buộc dựa vào split cụm.
- **Không đổi:** mục tiêu G2 vượt **0,7693** AUROC mức ô trên ma trận bão hòa, yêu cầu **thành phần kiến trúc mới** của [D-027](#d-027), baseline Degformer ở [D-028.8](#d-028), vai ba nhãn ở [D-031.2](#d-031). D-033 thêm trụ **cấp thiết** và trụ **phần mềm**; nó **không** thay trụ phương pháp và không tự làm G2 đạt.
- **Phạm vi bị thu hẹp so với hướng Trọng đã chuẩn y, và chỗ này cần Trọng xác nhận lại → [C-18](#c-18).** Hướng Claude đề xuất ở phiên này ban đầu lấy **đột biến lái ung thư** làm ví dụ dẫn. Phép đo trong cùng phiên **bác bỏ** ví dụ đó: trong 8 degron lái ung thư kinh điển chỉ **HIF1A** hiện ra, còn `CTNNB1` codon 31–48 **có số đo tốt và nói không phải degron** (PSI 5,27 / 5,36). Phạm vi đúng là **degron tự trị** và biến thể **dòng mầm**; mạch soma không có dữ liệu (cột `Oncogenicity` chỉ có 145 giá trị trong tile degron). Trọng ra lệnh **trước khi** có phép đo này nên việc thu hẹp là cách đọc của Claude, không phải điều Trọng đã quyết.
- **Hai kết quả âm phải đi kèm mọi lần trình bày con số 2,148:** (1) **không** có giàu lên theo *vị trí* — tỉ lệ biến thể trong degron bằng đúng tỉ lệ nền ở cả ba ngưỡng (33,4% so 32,4%; 13,2% so 12,8%; 3,9% so 3,8%) nên **không được nói “degron là điểm nóng biến thể”**; (2) ngưỡng PSI ≤ 3,0 cho **32,4% tile của toàn proteome** là degron, nên câu “biến thể nằm trong một degron” gần như không mang thông tin — giá trị phải đến từ dự đoán ΔPSI **theo residue**.
- **Đối chứng còn thiếu, đe doạ kết luận nhiều nhất:** chưa khử **bảo tồn** và **độ vô trật tự**. Nếu 2,148 biến mất sau khi khử thì nó chỉ nói “degron nằm trong vùng chức năng”. Phải chạy trước khi đưa con số vào đề cương; ghi ở [D](#theo-doi).

<a id="d-031"></a>

#### D-031 — Nhiệm vụ mức residue là trụ đóng góp

**15/10/2026 (phiên 8) · Trọng · Còn áp dụng.**

- **Còn áp dụng, khoản 2 và 4:** bộ quét học trục ngữ cảnh; bộ bão hòa xác nhận ma trận 19 thay thế; tile Voutsinos dùng cho chương đo lường cross-assay. Mục tiêu ma trận là vượt ΔPAP `cnn2w1` **0,7693 AUROC mức ô**, không lấy chênh lệch tới trần đo lường làm mức cải thiện hứa hẹn.
- **Khoản 1 và 3 — bằng chứng đã có:** hai việc chặn cũ đã xử lý; có delta dương trên bộ quét nhưng mô hình chuyển sang bão hòa vẫn thua ΔPAP. Đây chưa phải hoàn tất G2; xem [báo cáo](topics/degron-footprint/research/residue-task-derisk-2026-10-15/README.md) và [kết quả mô hình](topics/degron-footprint/research/residue-task-derisk-2026-10-15/model.json).
- **Khoản 5 — phát biểu:** thành phần ở thang lân cận ±3 thắng thành phần ở thang cả peptide. D-031.5 cũng yêu cầu đổi lý lẽ MIL sang giám sát yếu; trạng thái “đã yêu cầu” và “chờ xác nhận” trong hồ sơ C-17 cần [đối soát](#c-17), không tự duyệt thêm một thiết kế MIL.
- **Phạm vi thống kê:** MDE **0,0123** là ước lượng của cặp M3 − M0 trong [bảng lực §2.2](topics/degron-footprint/research/residue-task-derisk-2026-10-15/README.md), theo thiết kế ghép cặp hiện có; không phải ngưỡng đạt chung cho mọi ablation tương lai. Trần nhãn là **trần đo lường**.
- **Thay:** mục tiêu kiến trúc cross-assay của [D-027](#d-027), vai nhãn ở [D-028.5](#d-028), phần ưu tiên cross-assay và việc tính lực còn treo của [D-029](#d-029) / [D-030](#d-030). Không bỏ yêu cầu kiến trúc mới của D-027 hay baseline Degformer ở D-028.8.

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**15/10/2026 (phiên 8) · Trọng · Hiệu lực.** **Chấp nhận C-15 ([nguyên văn đề xuất](topics/degron-footprint/research/cross-assay-model-2026-10-15/README.md)): nhiệm vụ mức residue là trụ đóng góp; phần cross-assay hạ xuống một chương đo lường.** Trọng ra lệnh *"tiến hành thực hiện đề xuất C-15, nghiên cứu thêm để giảm thiểu rủi ro và trình bày được đóng góp rõ ràng"*. Báo cáo thực hiện: [residue-task-derisk-2026-10-15](topics/degron-footprint/research/residue-task-derisk-2026-10-15/README.md).

Năm hệ quả **đã đo xong trong cùng phiên**, nên quyết định này không còn kèm rủi ro mở như C-15 đã ghi:

1. **Hai việc chặn đóng lại.** Lực trên n = 91: **MDE 0,0123** ở lực 80% (ghép cặp theo peptide, bootstrap theo **89 cụm**), không phải 0,071 — con số cũ suy từ phương sai *không ghép cặp*. Rủi ro LeBlanc: **khoanh được**, tỉ lệ áp đảo của thành phần giảm từ ≈ **56×** (nhãn mức peptide) xuống **2,2×** (nhãn hiệu ứng đột biến), % hệ số ngữ cảnh tách khỏi 0 tăng **28,9% → 53,3%**.
2. **Thiết kế đánh giá thành ba nhãn ba vai, sửa [D-028](#d-028) mục 5.** Phát biểu "bộ bão hòa là nguồn **duy nhất** đỡ được mức residue" **không chính xác**: **bộ quét** cũng là nhãn hiệu ứng đột biến, và lớn hơn nhiều (**2.994 peptide / 1.985 cụm / 83.446 ô** so với 91 / 89 / 47.847). Vai đúng: bộ quét đỡ **trục ngữ cảnh**, bộ bão hòa đỡ **ma trận 19 thay thế**. ⇒ Câu "n = 91 là cỡ mẫu của phần mức residue" **phải bỏ**.
3. **Con số dương cho G2 đã có:** ngữ cảnh cục bộ ±3 đáng **+0,0289** AUROC so với lớp chỉ-thành-phần và **+0,0300** so với ΔPAP `cnn2w7`. ⇒ Điều kiện của [D-030](#d-030) mục 1 **đã đạt**. Nhưng tài liệu trình bày **vẫn chỉ làm khi Trọng yêu cầu**.
4. **Việc của kiến trúc đổi từ một câu sang một con số:** vượt **0,7693** AUROC mức ô của ΔPAP `cnn2w1` trên ma trận bão hòa (hiện thua **0,0420**), trần đo lường 0,9519, ngưỡng phát hiện **0,0123** đã tính trước. Ứng viên **"vị trí tuyệt đối trong peptide"** bị **loại** (+0,0002) — ứng viên thứ sáu bị loại bằng đo.
5. **Hai sửa câu chữ bắt buộc đi kèm**, ghi thành [C-17](#c-17): không nói "vị trí thắng thành phần" (phải nói **thang lân cận ±3** thắng **thang cả peptide**), và đổi lý lẽ cho MIL sang **giám sát yếu từ nhãn mức túi**.

**Ba chỗ câu chữ mà C-15 yêu cầu sửa đã xử lý:** (a) và (b) — mục A không còn con số **+0,1061** lẫn cụm "dư địa đến trần"; mọi trần nay gọi là **trần đo lường**. (c) nhánh stacking đã ghi là vô nghĩa do cộng tuyến ở [báo cáo cross-assay §3.1](topics/degron-footprint/research/cross-assay-model-2026-10-15/README.md). Các báo cáo phiên 3–4 **giữ nguyên làm lịch sử**, có ghi chú đính chính ở đầu.

</details>

<a id="d-030"></a>

#### D-030 — Điều kiện làm tài liệu, email giấy phép và SOURCE.md

**15/10/2026 · Trọng · Một phần; điều kiện làm tài liệu đã đạt.**

- **Khoản 1:** điều kiện có hướng đóng góp cụ thể và con số dương đã được D-031.3 ghi nhận là đạt trên nhiệm vụ residue. Ưu tiên huấn luyện **cross-assay** đã bị [D-031](#d-031) thay. Tài liệu trình bày vẫn làm theo yêu cầu của Trọng; nội dung phiên 9 đã được yêu cầu và cập nhật, xem [theo dõi](#tai-lieu-trinh-bay).
- **Khoản 2:** Trọng đã gửi email; **đang chờ trả lời**, không còn là việc “soạn/gửi email” chưa làm. Chỗ mơ hồ giấy phép trong [SOURCE.md](topics/degron-footprint/data/raw/larsen-2025/SOURCE.md) vẫn giữ đến khi có xác nhận; theo dõi tại [C-11a](#c-11a).
- **Khoản 3 còn áp dụng:** chỉ `data/README.md` và `SOURCE.md` trong `data/` được lên git. Khi sửa quy tắc ignore dữ liệu, kiểm `git check-ignore` và `git add -An` trước khi coi là xong. Chi tiết sự cố đã sửa giữ trong nguyên văn, không đưa lên phần A.

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**15/10/2026 · Trọng · Hiệu lực.** Ba việc.

1. **Chưa làm tài liệu trình bày với GVHD khi chưa chốt được hướng đi cụ thể về đóng góp.** **Thay mục tuần 6–7 của [D-029](#d-029)**: việc tài liệu **lùi lại** cho tới khi có một **hướng đóng góp cụ thể** — nghĩa là một đề xuất kiến trúc rõ ràng **kèm ít nhất một con số dương** trên nhiệm vụ cross-assay. Hệ quả: phần việc **mô hình cross-assay + kiến trúc** (vốn ở tuần 7–8) **lên trước**, và trở thành việc đang làm. Phần còn lại của D-029 (Larsen → chương residue → điểm kiểm tuần 10 → ứng dụng và viết) giữ nguyên thứ tự tương đối.

   Lý do Trọng nêu: trình bày một khung đóng góp chưa có hướng cụ thể thì không dùng được trong buổi gặp. Điều này **đảo** đánh đổi mà D-029 đã chọn (ưu tiên duyệt đề tài trước G2) — và nhận lại rủi ro ngược: GVHD vẫn chưa duyệt đề tài nào trong lúc tám tuần đang chạy.
2. **[C-11a](#c-11a) đã thực hiện** — Trọng **đã gửi email** xin xác nhận giấy phép MIT phủ cả file dữ liệu đầu ra. Đang **chờ trả lời**; cho tới khi có trả lời thì chỗ mơ hồ pháp lý vẫn ghi nguyên trong [SOURCE.md](topics/degron-footprint/data/raw/larsen-2025/SOURCE.md).
3. **`SOURCE.md` được lên git.** Đổi quy ước: **hai** loại file trong `data/` lên git, không còn một — `data/README.md` và `SOURCE.md` ở mọi độ sâu, để **thông báo giấy phép nguyên văn** đi theo repo. Đã sửa `.gitignore` và [CLAUDE.md](CLAUDE.md).

   ⚠ **Ghi lại một lỗi đã mắc và đã sửa trong cùng phiên:** bản sửa `.gitignore` đầu tiên của Claude (`!**/data/**/`) **mở chặn toàn bộ ~1,9 GB dữ liệu**, và bản thứ hai khiến nested git repo `voutsinos-2026/repo/` bị thêm thành **gitlink**. Bản cuối dùng `**/data/**` + `!**/data/raw/` + `!**/data/raw/*/` + `!**/data/**/SOURCE.md`, đã kiểm bằng `git check-ignore` và `git add -An` trên cả `topics/` và `archive/`: **chỉ** `data/README.md` và `SOURCE.md` được thêm. Lần sau đổi `.gitignore` của `data/` thì **bắt buộc** chạy `git add -An` trước khi coi là xong.

</details>

<a id="d-029"></a>

#### D-029 — Kế hoạch tám tuần và điểm kiểm tuần 10

**15/10/2026 · Claude (ủy quyền: Trọng “em tự xếp thứ tự”) · Một phần.**

- **Còn áp dụng:** điểm kiểm **cuối tuần 10**, sau đó ứng dụng và viết. Thứ tự hiện hành đọc ở [A](#hien-hanh) theo [D-031](#d-031), không thực hiện nguyên bảng tuần cũ.
- **Đã bị thay / đã làm:** tuần 6–7 đổi bởi [D-030.1](#d-030); mô hình cross-assay tuần 7–8 và lực còn treo tuần 9 đổi bởi [D-031](#d-031). Bộ Larsen đã tải; email đã gửi. Nội dung trình bày phiên 9 đã cập nhật; xem [D](#theo-doi).
- Phương án chuyển trọng tâm sang benchmark + ứng dụng ở điểm kiểm vẫn được giữ trong hồ sơ; nó không tự bãi bỏ G2 của [D-012](#d-012) hoặc yêu cầu kiến trúc của [D-027](#d-027).

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**15/10/2026 · Claude (ủy quyền: Trọng "em tự xếp thứ tự") · Hiệu lực; mục tuần 6–7 bị thay bởi [D-030](#d-030).** **Thứ tự tám tuần còn lại.** Căn cứ: rủi ro lớn nhất không phải kỹ thuật mà là **chưa đề tài nào được GVHD duyệt** sau khi năm phiên đo 15/10 đã đổi mốc cam kết, nhãn chính và định nghĩa việc-của-kiến-trúc; và G2 là cổng **duy nhất** chưa đạt.

| Tuần            | Việc                                                                                                                                | Ghi chú                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **6–7**   | **Tài liệu trình bày khớp trạng thái + ba câu hỏi cho GVHD** ([C-5](#c-5), và xác nhận [D-027](#d-027))              | ⚠ **Chờ Trọng bật đèn xanh**: Trọng đã dặn không tự sửa `presentation/` khi chưa được yêu cầu   |
| **7–8**   | **Mô hình cross-assay đầu tiên + thành phần kiến trúc mới** — nhắm vượt Spearman **0,7786** (trần 0,9778) | Đây là lần thử G2 thật đầu tiên. Kiến trúc nhắm **dịch chuyển định dạng assay** theo [D-027](#d-027) |
| **8**      | **[C-10](#c-10): tải bộ nhân Larsen → mức 5 của bậc thang** (chuyển ngăn tế bào)                                     | Rẻ (5,77 MB), mở rộng phần phân rã                                                                                   |
| **9**      | **Chương mức residue**: tính lực trên n = 91 rồi mô hình residue                                                      | Nhãn đột biến là nguồn **duy nhất** đỡ được mức residue ([D-028](#d-028) mục 5)                         |
| **10**     | **Điểm kiểm cứng** theo [C-12](#c-12)                                                                                       | Nếu chưa có con số vượt baseline thì chuyển trọng tâm sang benchmark + ứng dụng                                |
| **11–13** | **Ứng dụng** (API, ma trận 28×20, bất định neo vào trần nhãn, cờ ngăn tế bào) và **viết**                | Bốn tính năng đã kiểm là chỗ khác biệt duy nhất với năm tiền lệ                                             |

**Hai việc ngoài bảng, làm sớm khi tiện:** [C-11a](#c-11a) soạn email xin xác nhận giấy phép MIT — **Claude soạn nháp, Trọng đọc và tự gửi**, không tự gửi thay; và các việc câu chữ rẻ ở [C-12](#c-12).

**Điều thứ tự này nhận rủi ro:** đặt tuần 6–7 vào tài liệu nghĩa là **hoãn G2 thêm một tuần** trong khi không có dự phòng ([D-026](#d-026)). Đánh đổi có ý thức: tám tuần đặt trên một cách đóng góp GVHD chưa duyệt thì rủi ro hơn.

</details>

<a id="d-028"></a>

#### D-028 — Đánh giá, đối chứng và các đề xuất đã được nhận

**15/10/2026 · Trọng · Một phần; giữ số khoản của bản gốc.**

1. **Còn áp dụng:** cổng phơi lộ là cơ chế chuyển giao, ngoài đường găng G2.
2. **Còn áp dụng:** thước đo chính ma trận là **AUROC mức ô**.
3. **Còn áp dụng:** điểm kiểm cuối tuần 10. Hai việc chặn cũ đã xử lý theo [D-031.1](#d-031), không còn là đầu việc chờ.
4. **Còn áp dụng:** giữ split cụm **cov80**, không coi riêng split là tính mới. Trọng tâm kiến trúc xử lý dịch chuyển assay đã bị [D-031](#d-031) thay.
5. **Bị thay bởi D-031.2:** không còn gọi bộ bão hòa là nguồn duy nhất cho mức residue; ba nguồn có ba vai như D-031.
6. **Đã thực hiện:** tải bộ nhân Larsen; đánh giá chuyển assay/chuyển ngăn ở **mức tile**, không coi là nhãn residue hay test protein chưa thấy. Bằng chứng tải: [log phiên 6](topics/degron-footprint/log.md).
7. **Đã gửi, chờ trả lời:** email giấy phép [C-11a](#c-11a).
8. **Còn áp dụng:** **Degformer là baseline chính thức**; trích rõ “tự báo, chưa công bố, split ngẫu nhiên có 4,09% rò rỉ đo được”; 0,9162/0,9420 là **Pearson**. Giữ điều kiện nạp checkpoint pickle trong thư mục riêng bằng `python3 -I` như bản gốc. Chưa được bỏ đối chứng này chỉ vì vượt mốc ΔPAP.

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

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

</details>

<a id="d-027"></a>

#### D-027 — Khung đóng góp và yêu cầu kiến trúc mới

**15/10/2026 · Trọng · Một phần.**

- **Còn áp dụng:** nhận khung “đo và phân rã trần của một lớp bài toán”, đồng thời giữ **thành phần kiến trúc mới bắt buộc**. Đây là quyết định của **Trọng**, chưa phải GVHD duyệt; [C-5](#c-5) vẫn chờ thực hiện.
- **Bị thay bởi D-031:** nhiệm vụ kiến trúc xử lý dịch chuyển định dạng assay trên dải khó. Cross-assay nay là chương đo lường; mục tiêu kiến trúc chuyển sang residue / ma trận thay thế.
- Kết quả âm có thể hỗ trợ phân tích hoặc ablation; không tự thay đóng góp dương làm trụ theo [D-012](#d-012).

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**15/10/2026 (tối) · Trọng · Hiệu lực.** **Đóng góp dạng "đo và phân rã trần của một lớp bài toán" được nhận, nhưng đề tài **vẫn nên có kiến trúc mới**.** Giải quyết [C-7](#c-7) theo hướng **thuận có điều kiện** (không phải thay thế): mạch "benchmark + phân rã" được dùng làm **khung** của đóng góp, còn tính mới kiến trúc **vẫn là một thành phần bắt buộc**, không được bỏ. Hệ quả: cách đặt đóng góp ở [lập luận lại §7.1](topics/degron-footprint/research/topic-argument-2026-10-15.md) được nhận, nhưng **không** được dừng ở đó.

Hệ quả cho [C-13](#c-13): mạch H1 (phân rã khoảng cách qua assay) được giữ, và **phép đo ngày 15/10 vừa định nghĩa xong nhiệm vụ cho kiến trúc mới** — xem [báo cáo đo khoảng cách qua assay](topics/degron-footprint/research/reframe-options-2026-10-15/README.md) §9: khoảng cách qua assay là **0,0773 AUROC** (trần trong assay 0,9813 → qua assay 0,9041) và **gần như toàn bộ là hệ thống, không phải nhiễu** (hai assay đều rất tin cậy: 0,9749 và 0,9807; tương quan thật sau chỉnh suy giảm chỉ **0,7854**). Trên **dải khó** 2,0 < PSI < 4,0 thì AUROC qua assay rơi xuống **0,7839** và |r| xuống **0,5291**. ⇒ **Việc của kiến trúc mới là xử lý dịch chuyển định dạng assay, và phải được chấm trên dải khó**, không phải trên toàn dải.

Provenance đã xác nhận 15/10: **quyết định của chính Trọng**, không phải lời GVHD truyền đạt. Vì vậy [C-5](#c-5) **vẫn mở** — vẫn cần hỏi GVHD xác nhận ở buổi gặp, và câu hỏi nay gọn hơn: *đóng góp có khung "đo và phân rã" kèm một kiến trúc mới thì có đạt kỳ vọng không?*

</details>

<a id="d-026"></a>

#### D-026 — Không có đề tài dự phòng

**14/10/2026 · Trọng · Còn áp dụng.** `degron-footprint` là đề tài duy nhất; các ứng viên đã lưu trữ không giữ vai trò dự phòng. Giữ điểm kiểm G2 sớm vì chưa có đường lui được chuẩn bị.

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**14/10/2026 · Trọng · Hiệu lực.** **Chấp nhận không có đề tài dự phòng.** `degron-footprint` là đề tài duy nhất; các ứng viên đã lưu trữ ở D-024 không được giữ ở vai trò dự phòng. Hệ quả cần nhớ: nếu G2 không đạt thì không còn đường lui đã chuẩn bị, nên điểm kiểm G2 phải đặt sớm.

</details>

<a id="d-025"></a>

#### D-025 — Nhãn, split, chống chồng lặp và mốc precision@3

**14/10/2026 · Trọng · Một phần; giữ số khoản của bản gốc.**

1. **Còn đúng trong phạm vi precision@3 của bộ quét:** 0,4897 là mốc audit và 0,6514 là đối chiếu replicate; không gọi đây là baseline huấn luyện độc lập hay trần dự đoán phổ quát. 0,6045 và 0,7792 là oracle đọc nhãn test. Mục tiêu ma trận hiện hành ở [D-031](#d-031), không chuyển các số precision@3 sang AUROC.
2. **Bị thay bởi D-028.5 rồi D-031.2:** vai nhãn hiện là ba nguồn, ba vai. Điều kiện tính lực đã thực hiện trên tập bão hòa sau lọc 91 peptide / 89 cụm; không còn dùng 235 làm cỡ mẫu của tập này.
3. **Còn áp dụng:** nhãn trung bình hai replicate; báo kèm trần đo lường.
4. **Còn áp dụng:** split theo cụm protein **cov80**.
5. **Còn áp dụng:** peptide/cụm chồng giữa nguồn phải cùng phía train/test; phép chuyển nguồn phải loại cụm trùng khỏi train theo [D-031 và báo cáo](topics/degron-footprint/research/residue-task-derisk-2026-10-15/README.md). Số chồng lặp báo theo đúng tập lọc, không dùng cố định 130 cho mọi tập.
6. **Còn áp dụng:** nêu SVM Zhang 2023 và phân biệt phạm vi peptide/residue.
7. **Còn áp dụng:** không trộn BAG6 WT vào hai replicate chính.

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**14/10/2026 · Trọng · Hiệu lực.** **Xác nhận toàn bộ bảy đề xuất C-6** từ [audit dữ liệu 13/10 §9](topics/degron-footprint/research/full-data-audit/README.md):

1. Mục tiêu G2 phát biểu theo baseline thành phần trung thực **0,4897** và báo kèm trần nhãn **0,6514**; bỏ cách nói "vượt 0,6045 / +28,9%" (0,6045 và 0,7792 là oracle đọc nhãn test).
2. **Bộ bão hòa là nguồn nhãn chính**, bộ quét là nguồn phụ và để mở rộng độ phủ. Điều kiện kèm: tính lại lực cho 235 peptide **trước khi** cam kết thiết kế.
3. Nhãn là trung bình hai replicate; mọi bảng kết quả báo kèm trần nhãn.
4. Split theo cụm protein **cov80**.
5. 130 peptide có cả hai nguồn nhãn nằm cùng phía train/test.
6. Nêu SVM của Zhang 2023 trong G3 và đề cương, làm rõ khác phạm vi peptide/residue.
7. Không trộn mẫu BAG6 WT với hai replicate kia.

</details>

<a id="d-023"></a>

#### D-023 — Chọn đề tài degron-footprint

**12/10/2026 · Trọng · Một phần.**

- **Còn áp dụng:** `degron-footprint` là đề tài chính, nhiệm vụ footprint / hiệu ứng đột biến mức residue trên nhãn thực nghiệm.
- **Bị thay bởi D-024 / D-026:** A4 không còn là dự phòng; không còn năm ứng viên “đang đào sâu” chờ phân loại. Lý do lựa chọn và các số oracle giữ như bối cảnh tại thời điểm quyết; không dùng làm mốc G2 hiện hành.

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**12/10/2026 · Trọng · Hiệu lực; phần dự phòng bị thay bởi [D-024](#d-024).** **Đề tài chính là [`degron-footprint`](topics/degron-footprint/README.md)** (dự đoán footprint / hiệu ứng đột biến degron mức residue trên nhãn thực nghiệm). **Dự phòng là [`plm-calibration-audit`](archive/topics/plm-calibration-audit/README.md)** (A4, công cụ audit calibration và miền áp dụng). Thay vị trí đề tài chính ở [D-021](#d-021) ("chưa có đề tài chính") và vị trí dự phòng ở [D-016](#d-016) (degron là dự phòng duy nhất); giải quyết đề xuất C-4 phần đề tài chính/dự phòng.

Lý do: degron là ứng viên duy nhất có **khoảng trống đã chứng minh** chứ không phải "chưa kiểm" — 2.353/2.624 peptide (89,7%) có nhóm cùng cặp thay thế chứa cả vị trí dương và không dương, nên mô hình chỉ dùng thành phần amino acid **bị chứng minh không tách được**; cận trên chính xác của lớp mô hình đó là precision@3 0,6045, oracle không ràng buộc 0,7792 ([audit](topics/degron-footprint/research/composition-context-audit.md)). Thêm vào đó: G1 mạnh nhất repo, TC4 (XAI) được thỏa mãn bởi chính bài toán vì đầu ra là điểm quan trọng theo residue, có kiến trúc để đề xuất (mục 6 của audit), và dữ liệu đã nằm trên máy nên khả thi trong 8–9 tuần còn lại. A4 làm dự phòng vì G2 ít phụ thuộc kết quả âm nhất trong nhóm công cụ và G3 tự nhiên nhất, nay đã hợp lệ theo [D-022](#d-022).

**Chưa quyết (vẫn ở phần C):** vị trí của năm ứng viên còn lại — A2, A3, `dark-kinome-zero-shot`, `budgeted-plm-variant-scoring`, `scalable-metagenomic-binning`. Chúng giữ nguyên trạng "đang đào sâu" cho tới khi Trọng nói khác.

</details>

<a id="d-022"></a>

#### D-022 — Đóng góp dạng công cụ và nguồn xác nhận GVHD

**12/10/2026 · GVHD (Trọng truyền đạt) · Còn áp dụng, cần xác nhận lại.**

GVHD chấp nhận dạng công cụ/thước đo/audit/benchmark/tối ưu theo lời Trọng truyền đạt, **chưa có biên bản xác nhận riêng**. Với degron, đọc kèm [D-027](#d-027): vẫn phải có kiến trúc mới theo yêu cầu của Trọng; không suy ra rằng G2 hoặc ứng dụng được miễn. Hỏi lại GVHD theo [C-5](#c-5).

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**12/10/2026 · GVHD (Trọng truyền đạt) · Hiệu lực.** **GVHD chấp nhận đóng góp dạng công cụ** (công cụ, thước đo, audit, benchmark, thuật toán tối ưu) làm đóng góp của luận văn. Giải quyết đề xuất C-3 theo hướng thuận và **gỡ rào** cho các ứng viên A2, A3, A4, `budgeted-plm-variant-scoring`, `scalable-metagenomic-binning`.

Hệ quả: mức 3 của [D-017](#d-017) (ưu tiên tầng công cụ/benchmark/nền tảng) không còn mâu thuẫn với kỳ vọng của GVHD. Lời GVHD ngày 11/10 ("kỳ vọng một kiến trúc chưa ai dùng") vì vậy được đọc là **mong muốn, không phải điều kiện loại**; cả hai lời được giữ nguyên văn ở [people.md](project/people.md). Vẫn nên xác nhận lại ở buổi gặp tuần 6, vì đây là thông tin Trọng truyền đạt, chưa có biên bản.

Lưu ý điều **không** thay đổi: cổng [G2](project/course.md) vẫn đòi một đóng góp **dương** đo được — GVHD nhận dạng công cụ không có nghĩa là nhận kết quả âm ([D-012](#d-012)). Tiêu chí 5 (ứng dụng/website) vẫn không thể thiếu ([D-006](#d-006)).

</details>

<a id="d-012"></a>

#### D-012 — Ba cổng nghiên cứu G1/G2/G3

**10/10/2026 · Claude (khuyến nghị, được dùng làm chuẩn từ đó) · Còn áp dụng.** G1: nhãn thực nghiệm/chú giải độc lập; G2: đóng góp dương đo được; G3: ứng dụng khả thi. Giữ nguyên nguồn khuyến nghị trong hồ sơ, không gán thành lời GVHD trực tiếp. Định nghĩa: [course.md](project/course.md).

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**10/10/2026 · Claude (khuyến nghị), được dùng làm chuẩn từ đó · Hiệu lực.** Ba cổng bắt buộc: G1 nhãn độc lập, G2 đóng góp dương đo được, G3 ứng dụng khả thi. Định nghĩa đầy đủ ở [course.md](project/course.md).

</details>

<a id="d-006"></a>

#### D-006 — Năm tiêu chí GVHD và yêu cầu ứng dụng

**02/10/2026 · GVHD góp ý → Trọng · Còn áp dụng về tiêu chí.** Năm tiêu chí GVHD và yêu cầu ứng dụng/website vẫn dùng; xem [course.md](project/course.md) và [biên bản buổi gặp 1](project/meetings/2026-10-02-session-01/minutes.md). Phần rời hướng RTK–ATP chỉ còn giá trị lịch sử.

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**02/10/2026 (sau buổi gặp 1) · GVHD góp ý → Trọng · Hiệu lực.** RTK–ATP không bị từ chối, nhưng GVHD khuyên đổi sang đề tài khác. RTK–ATP coi như bỏ. Áp dụng **năm tiêu chí của GVHD**; tiêu chí 5 (ứng dụng/website) không thể thiếu. Biên bản: [minutes.md](project/meetings/2026-10-02-session-01/minutes.md).

</details>

<a id="quy-uoc-repo"></a>

### B2. Quy ước repo còn áp dụng

<a id="d-032"></a>

#### D-032 — Tổ chức lại sổ quyết định và đồng bộ quy ước

**15/10/2026 · Trọng · Còn áp dụng.** Trọng yêu cầu: *“áp dụng đề xuất trên vào repo, nhớ cập nhật cho CLAUDE.md còn AGENTS.md vẫn chỉ cần trỏ đến file claude.md như hiện tại”*.

- Áp dụng A ngắn; B1 nghiên cứu / B2 quy ước / B3 lịch sử thu gọn; C lựa chọn chờ xác nhận; D theo dõi thực hiện và phản hồi ngoài. Giữ toàn bộ mã D cũ và nguyên văn hồ sơ trong khối thu gọn; ghi rõ hiệu lực từng khoản ở bên ngoài.
- Sửa trạng thái tài liệu dựa trên bằng chứng đã có: ridge đã huấn luyện; bản nội dung slide đã cập nhật; email đã gửi nhưng chưa có phản hồi. Không ghi thêm kết quả nghiên cứu hay phê duyệt của GVHD.
- Phân biệt mốc ΔPAP với nghĩa vụ đối chứng Degformer, trần đo lường với dư địa dự đoán, MDE của phép so đã đo với điều kiện nghiệm thu chung. Không đổi thiết kế thí nghiệm trong lần biên tập này.
- **C-16 và C-17 không được tự đóng** bởi quyết định tổ chức tài liệu này. Mâu thuẫn phạm vi xác nhận của C-17 giữ rõ ở C; các việc GVHD/giấy phép chuyển sang D.
- Đồng bộ `CLAUDE.md`, liên kết và thẻ trạng thái; **giữ nguyên `AGENTS.md`**. Dùng anchor ổn định cho các phần; giữ điểm chuyển tiếp C → D để các liên kết cũ vẫn tra được.

<a id="d-020"></a>

#### D-020 — Dữ liệu đi theo thư mục đề tài

**12/10/2026 · Trọng · Còn áp dụng.** Không có `data/` ở gốc; dữ liệu nằm trong `topics/<ten-de-tai>/data/`, hoặc `archive/topics/<ten-de-tai>/data/` khi đóng đề tài. Giữ dữ liệu đã có; ngoại lệ lên git đọc kèm [D-030.3](#d-030).

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**12/10/2026 · Trọng · Hiệu lực.** Bỏ thư mục `data/` ở gốc. Dữ liệu của mỗi đề tài nằm trong chính thư mục đề tài, ở `topics/<ten-de-tai>/data/` (đề tài đã đóng: `archive/topics/<ten-de-tai>/data/`), và bị `.gitignore` chặn. Dữ liệu của đề tài đã đóng được giữ, không xoá.

</details>

<a id="d-019"></a>

#### D-019 — Nguồn quyết định duy nhất và tổ chức repo

**12/10/2026 · Trọng · Một phần.**

- **Còn áp dụng:** quyết định chỉ ghi tại file này; mỗi đề tài có thư mục riêng; các hướng đã đóng lưu trong `archive/`. Số đầu tên thư mục thể hiện thứ tự tiềm năng, **chỉ Trọng tự đặt**.
- **Bị thay bởi D-021 / D-024 / D-026:** danh sách sáu đề tài đang đào sâu và việc giữ RCA trong `topics/`.
- Các kết luận đóng đề tài được giữ làm lịch sử. Cách tổ chức sổ và cập nhật hiệu lực nay theo [D-032](#d-032).

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**12/10/2026 · Trọng · Hiệu lực; phần giữ RCA trong nhóm đang đào sâu bị thay bởi [D-021](#d-021).** Tổ chức lại repo. Từ nay quyết định chỉ ghi ở file này. Sáu đề tài đang đào sâu có thư mục riêng trong `topics/`: RCA, A2, A3, A4, degron, dark kinome zero-shot (mở lại hướng này). **Đóng hai đề tài không liên quan tin sinh học**: `legal-qa-grounding` và `personal-expense-management`. RCA vẫn giữ trong `topics/`. Các hướng cũ chuyển vào `archive/`. Thứ tự tiềm năng được mã hóa bằng số đầu tên thư mục, do Trọng tự đặt.

</details>

<a id="d-013"></a>

#### D-013 — HTML trong repo

**11/10/2026 · Trọng · Còn áp dụng.** Tạo HTML trong repo, mở bằng `file://`; không publish artifact.

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**11/10/2026 · Trọng · Hiệu lực.** Trang HTML được tạo trực tiếp trong repo và mở bằng `file://`, không publish artifact nữa.

</details>

<a id="d-004"></a>

#### D-004 — Repo private

**01/10/2026 · Trọng · Còn áp dụng.** Repo private; điều kiện chứa PDF và phân tích bài nhóm GVHD theo bản gốc. Khi đổi public phải xử lý các phần này cả trong lịch sử Git; quy ước chia sẻ chi tiết xem [CLAUDE.md](CLAUDE.md).

<details>
<summary>Nguyên văn hồ sơ trước khi tổ chức lại — chỉ để truy vết</summary>

**01/10/2026 · Trọng · Hiệu lực.** Repo GitHub chuyển sang private, nên được phép chứa PDF bài báo và phân tích về bài của nhóm GVHD. Nếu đổi sang public thì phải gỡ các phần này, kể cả khỏi lịch sử git.

</details>

<a id="lich-su"></a>

### B3. Lịch sử và bối cảnh

Các mục dưới đây không nằm trong kế hoạch degron đang thực hiện. “Lịch sử/bối cảnh” là vị trí tra cứu, **không tự hủy** quyết định đóng đề tài hoặc quyền chọn đầu vào đã được nêu. Câu “hiệu lực”, “đang đào sâu”, “chưa quyết” trong nguyên văn phải đọc theo ghi chú hiện hành đặt trước nó.

<details>
<summary>Mở 16 quyết định lịch sử và bối cảnh lựa chọn đề tài (D-024 về trước)</summary>

<a id="d-024"></a>

#### D-024

**Phân loại hiện hành:** Lưu trữ các ứng viên ngoài degron đã thực hiện; không còn nằm trong hàng đợi nghiên cứu. Hệ quả không dự phòng được giữ ở D-026.

**Nguyên văn hồ sơ:**

**14/10/2026 · Trọng · Hiệu lực.** **Lưu trữ mọi đề tài còn lại ngoài `degron-footprint`**: `plm-calibration-audit` (A4), `xai-fidelity-benchmark` (A2), `structure-sequence-leakage-audit` (A3), `dark-kinome-zero-shot`, `budgeted-plm-variant-scoring`, `scalable-metagenomic-binning` chuyển sang [archive/topics/](archive/README.md), giữ nguyên tài liệu, code và dữ liệu. Giải quyết đề xuất C-4. **Thay phần dự phòng của [D-023](#d-023)**: A4 không còn là dự phòng, hiện chưa có dự phòng; phần đề tài chính của D-023 giữ nguyên.

<a id="d-021"></a>

#### D-021

**Phân loại hiện hành:** RCA đã lưu trữ; mệnh đề “chưa có đề tài chính” bị D-023 thay. Không mở lại RCA từ bản ghi này.

**Nguyên văn hồ sơ:**

**12/10/2026 · Trọng · Hiệu lực; phần "chưa có đề tài chính" bị thay bởi [D-023](#d-023).** Lưu trữ đề tài `budgeted-microservice-rca` tại [archive/topics/budgeted-microservice-rca/](archive/topics/budgeted-microservice-rca/README.md), giữ toàn bộ tài liệu, code và dữ liệu đã có. **Hiện chưa có đề tài chính.** Thay vị trí đề tài chính ở D-016 và phần giữ RCA trong nhóm đang đào sâu ở D-019; giải quyết đề xuất C-1. Các nội dung còn lại của D-016 và D-019 giữ hiệu lực.

<a id="d-018"></a>

#### D-018

**Phân loại hiện hành:** Việc đào sâu A2/A3/A4 bị D-024 thay; không còn là đầu việc hiện hành.

**Nguyên văn hồ sơ:**

**12/10/2026 (tối) · Trọng · Hiệu lực.** Từ 14 ứng viên tầng công cụ trong [khảo sát](surveys/bioinformatics-tool-layer-candidates-2026-10-12.md), đi sâu ba ứng viên bậc A khớp GVHD: A2 (fidelity XAI), A3 (cấu trúc + trình tự, **phải thu hẹp** thành audit vì đã có Denger & Helms 2025), A4 (calibration/miền áp dụng). Nguồn: [journal 12/10](journal/2026-10.md).

<a id="d-017"></a>

#### D-017

**Phân loại hiện hành:** Bối cảnh tuyển đề tài, chưa bị bãi bỏ: ưu tiên tin sinh học; không bó residue/peptide; ưu tiên công cụ/benchmark/nền tảng; ngoài tin sinh học xếp sau. Chỉ cần tra khi xét lại phạm vi.

**Nguyên văn hồ sơ:**

**12/10/2026 · Trọng · Hiệu lực.** Định hướng chọn đề tài có 4 mức, tóm tắt ở phần A. Mục tiêu tối cao là tìm một đề tài có đóng góp thật, giải quyết vấn đề có ý nghĩa. Mục tiêu này đứng trên độ khớp với các ứng viên đang có.

<a id="d-016"></a>

#### D-016

**Phân loại hiện hành:** Lựa chọn RCA chính / degron dự phòng đã bị D-021, D-023 và D-026 thay.

**Nguyên văn hồ sơ:**

**12/10/2026 (chiều) · Claude (ủy quyền: "Claude tự quyết toàn bộ, chốt trong ngày") · Vị trí đề tài chính bị thay bởi [D-021](#d-021); vị trí dự phòng bị thay bởi [D-023](#d-023).** Chọn `budgeted-microservice-rca` làm đề tài chính, thay [D-014](#d-014). Degron là dự phòng duy nhất. Căn cứ: [báo cáo lựa chọn mở lĩnh vực](surveys/open-field-topic-selection-2026-10-12.md).

<a id="d-015"></a>

#### D-015

**Phân loại hiện hành:** Ứng viên legal QA đã bị D-016 thay và đóng ở D-019.

**Nguyên văn hồ sơ:**

**12/10/2026 · Trọng · Bị thay bởi D-016, đóng ở D-019.** Đưa `legal-qa-grounding` (hỏi–đáp pháp luật tiếng Việt) lên làm ứng viên hàng đầu ngoài lĩnh vực.

<a id="d-014"></a>

#### D-014

**Phân loại hiện hành:** Lựa chọn chính lần đầu đã bị D-016 thay; hiện chọn degron theo D-023. Mốc bỏ trục đặc hiệu E3 là lịch sử phạm vi.

**Nguyên văn hồ sơ:**

**11/10/2026 · Trọng · Bị thay bởi D-016.** Chốt degron làm đề tài chính. (Degron trở lại vị trí đề tài chính theo [D-023](#d-023), **không phải** vì mục này còn hiệu lực.) Khuya cùng ngày tái định tâm: bỏ trục đặc hiệu E3 (chỉ 1 E3 đủ mẫu), chuyển sang dự đoán footprint mức residue trên nhãn đột biến. Slug cũ `degron-e3-specificity`, nay là `degron-footprint`.

<a id="d-011"></a>

#### D-011

**Phân loại hiện hành:** Khuyến nghị dark kinome đã bị D-014 thay; kết luận về kết quả âm đọc theo D-012.

**Nguyên văn hồ sơ:**

**10/10/2026 · Claude (khuyến nghị) · Bị thay bởi D-014.** Khuyến nghị dark kinome trên DARKIN làm đề tài chính. Loại sirtuin khỏi vị trí chính vì Trọng cho biết **GVHD không nhận kết quả âm làm đóng góp chính**. Ngày 11/10, sáu phép kiểm đã làm sụp trụ tính mới (xem [thẻ đề tài](archive/topics/dark-kinome-zero-shot/README.md)).

<a id="d-010"></a>

#### D-010

**Phân loại hiện hành:** Giữ kết luận loại hướng sửa lỗi phần mềm; không chi phối việc thực hiện degron.

**Nguyên văn hồ sơ:**

**10/10/2026 · Trọng · Hiệu lực.** Loại hướng "sửa lỗi phần mềm có kiểm chứng".

<a id="d-009"></a>

#### D-009

**Phân loại hiện hành:** Lựa chọn sirtuin/kinase đã bị D-011 thay.

**Nguyên văn hồ sơ:**

**08/10/2026 · Claude (khuyến nghị) · Bị thay bởi D-011.** Đề tài chính là cơ chất deacetyl hóa theo isoform SIRT1–7, dự phòng là phospho theo nhóm kinase. Nguồn: [archive](archive/surveys/topic-final-recommendation.md).

<a id="d-008"></a>

#### D-008

**Phân loại hiện hành:** Giữ kết luận dừng TME senescence; bài học về nhãn được khái quát trong G1 ở D-012.

**Nguyên văn hồ sơ:**

**07/10/2026 · ghi trong nhật ký · Hiệu lực.** Dừng hướng TME senescence (scRNA-seq), vì điểm SenMayo là nhãn do chính pipeline sinh ra (trượt điều kiện về nhãn, về sau thành G1).

<a id="d-007"></a>

#### D-007

**Phân loại hiện hành:** Điều kiện đầu vào biểu hiện gene từng được chấp nhận theo Trọng truyền đạt; vẫn là bối cảnh hợp lệ nhưng không ràng buộc degron hiện tại.

**Nguyên văn hồ sơ:**

**07/10/2026 · GVHD · Hiệu lực.** GVHD chấp nhận đề tài có đầu vào là ma trận biểu hiện gene, không bắt buộc phải là chuỗi amino acid (theo Trọng truyền đạt).

<a id="d-005"></a>

#### D-005

**Phân loại hiện hành:** Lựa chọn trình RTK–ATP đã bị D-006 thay.

**Nguyên văn hồ sơ:**

**02/10/2026 · Trọng (tự chốt trước buổi gặp) · Bị thay bởi D-006.** Trình GVHD đề tài RTK–ATP.

<a id="d-003"></a>

#### D-003

**Phân loại hiện hành:** Giữ kết luận đóng IL-6 và lịch sử dự phòng efflux; không có vai dự phòng hiện tại.

**Nguyên văn hồ sơ:**

**01/10/2026 · Trọng · Hiệu lực (đã đóng).** Loại hướng peptide IL-6. Efflux giữ làm dự phòng cho RTK–ATP, sau đó bỏ cùng RTK–ATP.

<a id="d-002"></a>

#### D-002

**Phân loại hiện hành:** Bối cảnh chuyển sang tin sinh học; quản lý chi tiêu đã đóng ở D-019. Hướng hiện tại đọc D-023.

**Nguyên văn hồ sơ:**

**01/10/2026 · Trọng · Hiệu lực.** Chuyển sang lĩnh vực tin sinh học (chuyên môn GVHD). Tạm dừng đề tài quản lý chi tiêu; đề tài này đóng hẳn ở D-019.

<a id="d-001"></a>

#### D-001

**Phân loại hiện hành:** Đề tài quản lý chi tiêu đã bị D-002 thay và đóng ở D-019.

**Nguyên văn hồ sơ:**

**24–29/09/2026 · Trọng · Bị thay bởi D-002.** Đề tài quản lý chi tiêu cá nhân có bộ phân loại giao dịch tự thích nghi.

</details>

<a id="cho-xac-nhan"></a>

## C. Đề xuất chờ xác nhận

Chỉ chứa lựa chọn hoặc phạm vi phê duyệt còn thiếu; việc đã được giao nhưng chưa xong nằm ở [D](#theo-doi). Mỗi đề xuất nêu câu hỏi cần quyết, khuyến nghị, ảnh hưởng và điều kiện còn thiếu. Không đưa kết quả đo vào C như thể nó cần được biểu quyết mới đúng.

> ✅ **15/10/2026 (phiên 10) — hàng đợi C đã trống.** Cả bốn mục **C-16, C-17, C-18, C-19** đã được giải quyết bởi [D-035](#d-035) theo ủy quyền của Trọng. Bốn mục dưới đây **giữ nguyên để truy vết**, mỗi mục có một dòng ghi kết quả ở đầu; chúng **không còn là hàng đợi chờ duyệt**.
>
> Hai việc còn chờ **bên ngoài**, không phải lựa chọn của Trọng hay Claude, nằm ở [D](#theo-doi): [C-5](#c-5) (GVHD duyệt khung, buổi gặp 16/10) và [C-11a](#c-11a) (chờ email trả lời về giấy phép).

<a id="c-18"></a>

### C-18 — Xác nhận lại phạm vi đã bị thu hẹp của D-033

> ✅ **ĐÃ NHẬN** — [D-035](#d-035), 15/10/2026, Claude (ủy quyền). Phạm vi là **degron tự trị + biến thể dòng mầm**; bỏ “đột biến lái ung thư” khỏi mạch dẫn nhập.

**Claude đề xuất 15/10/2026 (phiên 10) · Đã được giải quyết.** Câu cần quyết: phạm vi mạch cấp thiết là **degron tự trị + biến thể dòng mầm**, đúng không?

Trọng ra lệnh thực hiện “hướng vừa đề xuất” **trước khi** có phép đo ở mục 7 của [báo cáo](topics/degron-footprint/research/variant-coverage-2026-10-15/README.md). Hướng đó khi được nêu lấy **đột biến lái ung thư** làm ví dụ dẫn, và phép đo đã **bác bỏ ví dụ đó**: trong 8 degron lái ung thư kinh điển chỉ **HIF1A** hiện ra (PSI 1,86 / 1,51, MLN4924 đẩy lên 2,45); `CTNNB1` codon 31–48 **đo tốt mà không phải degron** (reads 145/66, PSI 5,27 / 5,36); `MYC` T58/S62 **vắng mặt khỏi thư viện**; `NFE2L2` ETGE không phải degron. Cách đọc: assay GPS phát hiện degron **tự trị** trong 28-mer, còn degron **có điều kiện** (phụ thuộc phosphoryl hóa hay cần nhiều motif) nằm ngoài tầm.

**Khuyến nghị:** nhận phạm vi **degron tự trị**, **biến thể dòng mầm**; **bỏ** mọi cách nói “đột biến lái ung thư” khỏi mạch dẫn nhập. Ảnh hưởng: con số cấp thiết 2,148 **không đổi** (nó tính trên nhãn dòng mầm), chỉ ví dụ dẫn đổi. Nếu giữ mạch ung thư thì phải nói kèm rằng chính assay của đề tài không thấy 7/8 degron lái ung thư — tự hạ đề tài trước hội đồng.

Điều kiện còn thiếu: ⚠ mạch soma **không có dữ liệu** — cột `Oncogenicity` của ClinVar chỉ có ~800 giá trị trên 2,56 triệu biến thể missense, trong đó 145 trong tile degron, **5** trong bộ quét, **0** trong bộ bão hòa.

<a id="c-19"></a>

### C-19 — Có còn dùng C-16 làm đối chứng ngoài không?

> ✅ **ĐÃ NHẬN** — [D-035](#d-035), 15/10/2026, Claude (ủy quyền). [C-16](#c-16) chuyển sang **không dùng**. ⚠ Giá phải trả: rủi ro “cả hai nguồn nhãn mức residue đều của Zhang 2023” **vẫn mở, chưa có ứng viên thay thế**; yêu cầu cho ứng viên mới ghi ở D-035.

**Claude đề xuất 15/10/2026 (phiên 10) · Đã được giải quyết.** Câu cần quyết: [C-16](#c-16) có nên chuyển sang **không dùng** không?

Phép đo phiên 10 nhắm đúng tile mà C-16 dựa vào: tile 2 của `P35222` (residue 24–51, chứa trọn codon 31–48). Tile đó **có trong peptidome GPS, đo tốt** (reads 145 rep1 / 66 rep2) và **PSI 5,27 / 5,36** — tức **bền**, cách ngưỡng degron 3,0 rất xa. ⇒ Dùng Krishna 2026 làm đối chứng hội tụ sẽ cho kết quả **âm vì lý do assay** (degron β-catenin cần phosphoryl hóa trong phức hủy, không tự trị trong 28-mer), **không** vì mô hình sai — và hai nguyên nhân đó **không phân biệt được** bằng thí nghiệm này.

**Khuyến nghị:** chuyển C-16 sang **không dùng**, ghi lý do là bằng chứng đo được, không phải vấn đề giấy phép. Ảnh hưởng: rủi ro *“cả hai nguồn nhãn mức residue đều của một nhóm tác giả (Zhang 2023)”* **vẫn mở** và cần ứng viên khác — ưu tiên một bộ đo **độ bền** (không phải tín hiệu Wnt) trên **degron tự trị**. Việc này không chặn G2.

<a id="c-16"></a>

### C-16 — Có bổ sung đối chứng ngoài CTNNB1 không?

> ❌ **KHÔNG DÙNG** — [D-035](#d-035) qua [C-19](#c-19), 15/10/2026, Claude (ủy quyền). Căn cứ là **bằng chứng đo được** (tile 24–51 của `P35222` đo tốt và **không phải degron**, PSI 5,27 / 5,36), **không** phải vấn đề giấy phép. Nội dung dưới đây giữ làm lịch sử.

**Claude đề xuất 15/10/2026 · Đã được giải quyết.** Khuyến nghị xem dữ liệu Krishna 2026 là **đối chứng hội tụ ngoài**, không là nhãn độ bền cùng loại hay tập huấn luyện. Giá trị dự kiến: kiểm tra ngoài nhóm dữ liệu Zhang 2023. Trước khi dùng phải kiểm được bảng điểm và giấy phép; readout là **tín hiệu Wnt**, chỉ có một degron. Nguồn, số biến thể và kiểm protein/tile: [báo cáo §8](topics/degron-footprint/research/residue-task-derisk-2026-10-15/README.md).

> ⚠ **Bằng chứng mới, phiên 10 (15/10):** tile mà đề xuất này dựa vào — residue 24–51 của `P35222`, chứa trọn codon 31–48 — **có trong peptidome GPS, đo tốt và không phải degron** (reads 145/66, PSI **5,27 / 5,36**). Điều này làm C-16 **yếu đi nhiều** và sinh ra [C-19](#c-19) hỏi có nên chuyển sang *không dùng*. Câu *“`P35222` không có trong bảng PSI của Zhang”* trong hồ sơ gốc dưới đây đúng với **bảng quét/bão hòa**, nhưng **không đúng** với peptidome GPS. Không tự đóng C-16 bằng ghi chú này; quyết định thuộc Trọng.

<details>
<summary>Nội dung đề xuất gốc và căn cứ chi tiết</summary>

| #    | Đề xuất                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Người đề xuất | Ghi chú                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C-16 | **Dùng dữ liệu `CTNNB1` của Krishna 2026 làm đối chứng ngoài, độc lập.** *Nature Genetics* 58:366–375, DOI [10.1038/s41588-025-02496-5](https://doi.org/10.1038/s41588-025-02496-5): saturation genome editing tại locus nội sinh, **cả 342 đột biến missense** trên **codon 31–48** của degron β-catenin. Độc lập theo cả ba trục: nhóm tác giả khác, **assay khác**, **protein chưa thấy** (`P35222` **không** có trong bảng PSI của Zhang, **không** có trong thư viện TF của Larsen — đã kiểm). Và khớp đúng khuôn: codon 31–48 nằm **trọn** trong tile 2 của `P35222` (residue 24–51 theo quy tắc `(n−1)·23`) nên chấm được bằng đúng mô hình 28-mer hiện có. Giá trị: đóng rủi ro **cả hai nguồn nhãn mức residue đều của một nhóm tác giả (Zhang 2023)** | Claude, 15/10/2026 | ⚠ **Ba điều phải kiểm trước:** (a) readout là **tín hiệu Wnt**, không phải độ bền ⇒ chỉ gọi được là **đối chứng hội tụ**, không phải nhãn cùng loại; (b) **giấy phép chưa rõ** — bảng điểm từng biến thể nằm ở *Source data*/Supplementary, phần deposit công khai (GEO `GSE299075`, EGA `EGAS00001005364`) là RNA-seq chứ không phải điểm, code ở Zenodo mà [resources §4](resources/README.md) ghi **Zenodo trả 403 từ mạng này**; (c) **342 ô / 1 degron / 18 vị trí** ⇒ đủ làm đối chứng, **không** đủ huấn luyện. Chi tiết: [báo cáo §8](topics/degron-footprint/research/residue-task-derisk-2026-10-15/README.md) |

</details>

<a id="c-17"></a>

### C-17 — Đối soát phạm vi xác nhận của lý lẽ MIL và phát biểu ngữ cảnh

> ✅ **ĐÃ NHẬN cả (a) và (b)** — [D-035](#d-035), 15/10/2026, Claude (ủy quyền). (a) lý lẽ MIL đổi sang **giám sát yếu từ nhãn mức túi**, bỏ cách nói “chưa tìm thấy tiền lệ” làm căn cứ tính mới; (b) phát biểu **“thành phần ở thang lân cận ±3 thắng thành phần ở thang cả peptide”**. ⚠ Nhận (a) **không** duyệt một thiết kế MIL cụ thể — vẫn phải qua ablation.

**Claude đề xuất 15/10/2026 · Đã được giải quyết.** Hồ sơ trước tổ chức lại vừa ghi “chờ xác nhận”, vừa có [D-031.5](#d-031) yêu cầu cả hai sửa đổi. [D-032](#d-032) chỉ tổ chức tài liệu, không tự biến một đề xuất kiến trúc thành quyết định.

- <a id="c-17a"></a>**(a) Lý lẽ MIL:** D-031.5 đã yêu cầu đổi sang **giám sát yếu từ nhãn mức túi**. Phần còn cần làm rõ là trạng thái xác nhận của đề xuất gốc và phạm vi thử nghiệm cụ thể; không dùng “chưa tìm thấy tiền lệ” để tuyên bố tính mới. Chưa suy ra một thiết kế MIL cụ thể đã được duyệt.
- <a id="c-17b"></a>**(b) Phát biểu theo số đo:** thực hiện D-031.5 bằng câu “**thành phần ở thang lân cận ±3 thắng thành phần ở thang cả peptide**”. Đây là việc đồng bộ theo bằng chứng; bản nội dung slide đã áp dụng, xem [theo dõi](#tai-lieu-trinh-bay).

Câu trả lời âm cho một nhánh MIL có thể hỗ trợ phân tích/ablation, không thay yêu cầu đóng góp dương làm trụ của [D-012](#d-012) / [D-027](#d-027). Tránh dùng “ít nhãn = 89 cụm” cho toàn bộ nhiệm vụ residue: bộ quét còn đỡ trục ngữ cảnh theo D-031.2.

<details>
<summary>Nội dung đề xuất gốc và căn cứ chi tiết</summary>

| #    | Đề xuất                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Người đề xuất | Ghi chú                                                                                                                                                                                                                        |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C-17 | **Đổi lý lẽ cho phần MIL của kiến trúc, và đổi luôn phát biểu "trục vị trí".** Hai sửa: (a) bỏ cách nói *"MIL so với đầu theo vị trí — chưa tìm thấy tiền lệ"*, vì tra y văn 15/10 cho thấy mô típ chuẩn là **đầu theo residue khi có nhãn mức residue, MIL khi chỉ có nhãn mức túi** ⇒ đặt MIL làm tính mới là **yếu**. Lý lẽ thay thế, có số đỡ: **giám sát yếu** — nhãn mức túi (GPS 260k peptide, tile 212k) **rất dồi dào nhưng không nhận diện được tham số vị trí** (28,9%), nhãn mức ô **nhận diện được nhưng ít** (89 cụm) ⇒ câu hỏi kiến trúc là *cầu nối MIL/attention có moi được thông tin mức residue từ nhãn mức túi hay không*, và **câu trả lời âm cũng dùng được**. (b) Mọi chỗ viết "vị trí thắng thành phần" sửa thành **"thành phần ở thang lân cận ±3 thắng thành phần ở thang cả peptide"** — theo phân rã +0,0232 / +0,0057 / +0,0002 | Claude, 15/10/2026 | Mục (b) là **sửa câu chữ bắt buộc** nếu [D-031](#d-031) có hiệu lực, vì nếu không thì đề tài phát biểu sai chính phép đo của mình. Mục (a) đổi **lý do**, không đổi việc phải làm |

</details>

### Tra cứu đề xuất đã xử lý

Các điểm chuyển tiếp giữ mã C cũ để liên kết trong báo cáo và hồ sơ vẫn có đích. Chúng không phải hàng đợi chờ duyệt.

| Mã cũ                 | Nơi ghi kết quả                                                           |
| ----------------------- | ---------------------------------------------------------------------------- |
| <a id="c-1"></a>C-1     | Lưu trữ RCA: [D-021](#d-021)                                                |
| <a id="c-3"></a>C-3     | Đóng góp dạng công cụ: [D-022](#d-022)                                  |
| <a id="c-4"></a>C-4     | Chọn đề tài rồi lưu trữ ứng viên: [D-023](#d-023), [D-024](#d-024)    |
| <a id="c-6"></a>C-6     | Bảy đề xuất audit nhãn: [D-025](#d-025); đọc các khoản đã bị thay |
| <a id="c-7"></a>C-7     | Khung đóng góp kèm kiến trúc: [D-027](#d-027)                           |
| <a id="c-8"></a>C-8     | Cổng phơi lộ ngoài đường găng: [D-028.1](#d-028)                      |
| <a id="c-9"></a>C-9     | AUROC mức ô: [D-028.2](#d-028)                                              |
| <a id="c-10"></a>C-10   | Bộ nhân Larsen đã tải: [D-028.6](#d-028)                                 |
| <a id="c-11b"></a>C-11b | Baseline Degformer: [D-028.8](#d-028)                                         |
| <a id="c-12"></a>C-12   | Kiểm rủi ro / tuần 10: [D-028.3](#d-028), [D-031](#d-031)                   |
| <a id="c-13"></a>C-13   | Vai nhãn: [D-028.5](#d-028), đã được [D-031.2](#d-031) thay              |
| <a id="c-14"></a>C-14   | Giữ cov80: [D-028.4](#d-028)                                                 |
| <a id="c-15"></a>C-15   | Trụ đóng góp residue: [D-031](#d-031)                                     |
| C-16                    | **Không dùng** đối chứng `CTNNB1`: [D-035](#d-035) qua [C-19](#c-19)         |
| C-17                    | Lý lẽ MIL + phát biểu thang lân cận: [D-035](#d-035)                         |
| C-18                    | Phạm vi degron tự trị + dòng mầm: [D-035](#d-035)                           |
| C-19                    | Bỏ đối chứng `CTNNB1`: [D-035](#d-035)                                        |

<a id="theo-doi"></a>

## D. Theo dõi thực hiện và xác nhận bên ngoài

Đây là trạng thái triển khai của việc đã có căn cứ, không phải một nơi ghi quyết định mới hoặc bản sao toàn bộ backlog. Việc mô hình/ứng dụng chi tiết nằm trong [README](topics/degron-footprint/README.md) và [log đề tài](topics/degron-footprint/log.md).

<a id="c-5"></a>

### C-5 — Hỏi GVHD xác nhận khung đóng góp

**Chưa thực hiện; buổi gặp ngày 16/10/2026 — mục đích là XIN DUYỆT KHUNG đề tài** (Trọng nêu 15/10). Câu hỏi nay gọn lại thành **xin duyệt khung ba trụ**:

1. **Cấp thiết** — vùng degron giàu biến thể gây bệnh **2,148×** so với lành tính, khử nhiễu theo protein ([D-033](#d-033)). ⚠ Nói kèm: chưa khử bảo tồn/vô trật tự.
2. **Phương pháp** — nhiệm vụ mức residue, **kèm thành phần kiến trúc mới** ([D-031](#d-031), [D-027](#d-027)). G2 **chưa đạt**; mục tiêu vượt 0,7693.
3. **Phần mềm** — dịch vụ dự đoán có bất định + harness đánh giá ([D-033](#d-033)); GVHD **đã xác nhận bằng lời** là đóng góp ([D-034](#d-034)).

**Hai việc phải lấy về từ buổi gặp:** (a) **biên bản** cho lời xác nhận ở [D-034](#d-034) — hiện chỉ là thông tin Trọng truyền đạt, như lời 12/10 ở [D-022](#d-022); (b) xác nhận đề tài **được duyệt** hay chưa — tới nay **chưa có căn cứ** nào ghi là đã duyệt. Khi có phản hồi: lưu nguyên văn vào biên bản `project/meetings/`, chỉ ghi **hệ quả** thành D mới.

<a id="c-11a"></a>

### C-11a — Phản hồi giấy phép dữ liệu Larsen

**Email đã gửi 15/10/2026; đang chờ trả lời** theo [D-030.2](#d-030). Không còn việc soạn/gửi lại trong hàng đợi. Giữ nguyên chỗ mơ hồ trong [SOURCE.md](topics/degron-footprint/data/raw/larsen-2025/SOURCE.md); khi nhận phản hồi mới cập nhật nguồn và trạng thái. Không ghi “giấy phép đã hoàn tất” chỉ vì repo tác giả có MIT.

<a id="doi-chung-cap-thiet"></a>

### Đối chứng cho con số cấp thiết 2,148

**Chưa chạy.** Theo [D-033](#d-033), tỉ số chênh **2,148** chưa khử **bảo tồn** và **độ vô trật tự**. Vùng degron chồng lấn với vùng vô trật tự, vị trí PTM và motif tuyến tính ngắn, nên chưa nói được *“gây bệnh vì phá degron”* — chỉ nói được *“degron giàu biến thể gây bệnh”*. Cách làm: thêm bảo tồn (phyloP/ConSurf) và rASA/pLDDT làm tầng phân tầng thứ hai trong cùng khuôn Mantel–Haenszel của [`enrichment.py`](topics/degron-footprint/research/variant-coverage-2026-10-15/enrichment.py). **Phải chạy trước khi đưa con số vào đề cương.** Hai việc nhỏ đi kèm: ghim bản ClinVar archive tháng 10/2026 ([SOURCE.md §5](topics/degron-footprint/data/raw/clinvar/SOURCE.md)) và đếm chồng lặp giữa 575 và 1.037 để con số ≈1.600 thành chính xác.

<a id="tai-lieu-trinh-bay"></a>

### Tài liệu trình bày

**Nội dung đã cập nhật sau phiên 11 theo khung ba trụ; chưa dựng HTML/PPTX.** Brief nay có **26 slide**: thêm phần **Product** (slide 23–24), slide 6 viết lại quanh con số 2,148 ở **mức vùng**, và các ràng buộc câu chữ của [D-036](#d-036) đã áp vào mọi chỗ nhắc ClinVar. Bảng đính chính và bảng việc còn lại nằm ở [slide-content-2026-10-15.md](topics/degron-footprint/presentation/slide-content-2026-10-15.md); nguồn trạng thái là [log phiên 11](topics/degron-footprint/log.md). **Trang khung mang đi buổi gặp 16/10 đã có**: [framework-one-pager.html](project/meetings/2026-10-16-session-02/framework-one-pager.html) (bản in A4) kèm [bản Markdown](project/meetings/2026-10-16-session-02/framework-one-pager.md). **Còn lại:** bốn câu hỏi xin GVHD — ở slide 26 của brief và ở trang khung — **Trọng tự viết**. Cảnh báo cũ “năm chỗ chưa sửa” đã hết hạn và được bỏ khỏi A. `presentation.html` và `session-02-prep.md` là hai bản 11/10 giữ để đối chiếu, không dùng làm tài liệu hiện hành. Công việc trình bày tiếp theo vẫn theo yêu cầu của Trọng ([D-030](#d-030), [D-031](#d-031)).
