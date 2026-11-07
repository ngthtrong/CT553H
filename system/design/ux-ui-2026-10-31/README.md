# Phân tích UX/UI và thiết kế Figma — 31/10/2026

> **Bản cũ — không dùng để duyệt UI hiện tại.** Người dùng đã yêu cầu thiết kế lại và chọn hướng B ngày 01/11/2026. Mở [Workspace UI v2](../workspace-ui-v2/index.html). Gói và bản ghi Figma bên dưới chỉ giữ làm lịch sử; không tiếp tục import bản này.

**Trạng thái:** thiết kế đề xuất dựa trên phạm vi BA v0.2 ngày 29/10/2026. Đây là bộ thiết kế và prototype để review; không phải chức năng đã triển khai, kết quả nghiên cứu mới hay nghiệm thu G2/G3.

**Bản review đầy đủ:** [review.html](review.html) — mở trực tiếp bằng trình duyệt; đã nhúng font, icon và artwork, không cần mạng. Có 47 khung: 19 desktop, 23 trạng thái/hộp thoại, 3 mobile, 2 bảng định hướng. Menu và hotspot chuyển giữa các ví dụ cố định; không thực thi nghiệp vụ thật.

**Figma hiện tại:** [Degron Footprint · Research Workspace](https://www.figma.com/design/MdMLYZQfXqGcL3br3JMunM) mới có **41 token local, 10 text style và 8 component nền**. Đợt ghi màn hình không commit; sau đó MCP báo hết quota Starter. **Chưa có 47 màn hình trên Figma.** Không có kiểm tra ảnh Figma sau dựng màn hình.

**Tiếp tục nhập:** [gói native development plugin](figma-import-package.zip), [hướng dẫn](figma-plugin/README.md). Plugin lấy node spec từ bản review và tạo text/vector/auto-layout/components có thể chỉnh sửa, bằng thao tác chạy plugin trong Figma Desktop. Cần manifest có ID thật do Figma cấp; template chưa cấu hình không nhập trực tiếp được. Native import chưa được chạy/kiểm tra, không được coi là đã hoàn thành phần Figma.

`figma-manifest.json` phân biệt phần đã ghi, phần chờ nhập và kiểm tra cục bộ; `screen-map.json` liên kết các màn hình với UC/FR và acceptance tham chiếu.

## 1. Cơ sở phân tích và thứ tự ưu tiên

Đã đối chiếu [README hệ thống](../../README.md), [SRS](../../srs.md), [thiết kế dữ liệu](../../db-design.md), [API](../../api-spec.md), [OpenAPI](../../openapi.yaml), [wireframe BA](../../ui-design.md), [kế hoạch kiểm thử](../../test-plan.md), [bản ghi đồng bộ phạm vi](../../scope-validation-2026-10-29.md), [deviations của baseline](../../app/DEVIATIONS.md), CSS/router hiện có và [đề cương](../../../proposal/proposal.md). Phạm vi phần mềm hiện tại trong SRS/README v0.2 được ưu tiên khi đề cương hay mã baseline còn mô tả phạm vi cũ.

| Điều đã xác định từ BA | Hệ quả thiết kế |
|---|---|
| Một ứng dụng local, một người vận hành, không tài khoản | Không thêm đăng nhập, phân quyền, thành viên hay chia sẻ công khai. Navigation xoay quanh công việc nghiên cứu. |
| Đơn vị dự đoán là peptide 28 residue, 532 phép thay thế | Màn hình protein là điều phối nhiều tile; mỗi kết quả vẫn có tile và ngữ cảnh riêng. |
| UC-01–10 đều thuộc bản đầu | Thiết kế đồng thời dự án/lịch sử, lô/protein, nhập/so sánh và các luồng baseline. |
| Preview tạm thời; save/submit/commit là các thời điểm lưu bền | Đặt thông báo lưu ngay cạnh hành động; lịch sử không tự hết hạn. |
| Kết quả phát triển, chưa xác nhận độc lập | Nhãn bằng chứng luôn nằm trước biểu đồ; không dùng từ “đã xác thực” cho dự đoán/import. |
| Domain gate R3 chưa tích hợp đầy đủ trong baseline | Thiết kế bao phủ target `borderline` và nguồn gate; không lấy trạng thái hiện tại của baseline làm bằng chứng target đã chạy. |
| Số đo, xác suất, score và ClinVar khác bản chất | Tách nhãn, đơn vị, thang màu và vị trí hiển thị. |

Các giá trị dự đoán, số lượng công việc và dữ liệu import trong mockup là **fixture minh hoạ thiết kế**. Chuỗi `DIMFLVDSSGSIGPENFSKMKTFMKNLV`, accession A6NMZ7 và quy tắc tọa độ được lấy từ tài liệu BA. Fixture không được đưa vào benchmark hoặc mô tả như số đo thật.

## 2. Nhu cầu người dùng và công việc cốt lõi

Persona dưới đây là **giả thuyết thiết kế rút ra từ stakeholder của SRS**, chưa phải kết quả phỏng vấn.

1. Nhà nghiên cứu sinh học cần chọn một danh sách phép thay thế có thể đem đi kiểm chứng, hiểu đúng chiều tác động và biết khi nào mô hình không đủ căn cứ.
2. Nhà nghiên cứu tính toán cần xử lý nhiều đầu vào, kiểm tra item lỗi và lấy toàn bộ kết quả có provenance, không phải chụp ảnh heatmap.
3. Người thực hiện luận văn cần mở lại đúng phiên bản phân tích, đối chiếu số đo và giải trình tại sao một kết quả có hoặc không có chú giải.

Job chính: “Từ peptide/protein và các quan sát đang có, chọn phép thay thế đáng kiểm tra tiếp, đồng thời giữ đủ ngữ cảnh để giải thích và tái lập lựa chọn.”

Điểm kết thúc của công việc là shortlist/xuất dữ liệu có bối cảnh và nguồn gốc; số dashboard hay độ đẹp của heatmap không tự thể hiện thành công khoa học.

## 3. Phân tích các điểm khó của BA

| Rủi ro nhận thức/thao tác | Quyết định UX | Tiêu chí review |
|---|---|---|
| Đọc xác suất như nguy cơ bệnh | Viết `P(ΔPSI ≥ 1.0)` ngay cạnh giá trị; mô tả “PSI tăng ≥ 1 bin; tín hiệu degron yếu đi trong assay này”. ClinVar nằm trong panel chú giải riêng. | Người xem nói lại đúng sự kiện; không diễn giải bệnh lý từ heatmap. |
| Thấy số rồi mới đọc giới hạn | Thứ tự header → domain → warnings → evidence → controls → scores. Banner cảnh báo không có nút đóng. | Giới hạn xuất hiện trước số trên desktop và mobile. |
| `unknown` bị xem như `out` hoặc “an toàn” | Trạng thái bằng chữ: in/out/borderline/unknown/unreliable; nguồn measured/predicted riêng. `out` từ chối mặc định. | Người xem phân biệt “không biết” với “đã biết ngoài miền”. |
| Protein dài tạo cảm giác dự đoán cả protein | Coverage có khoảng không phủ, tile lỗi và cửa sổ chồng lấn. Ranking luôn trong tile. | Không có điểm toàn protein hay trung bình ngầm các ngữ cảnh. |
| Job “hoàn tất” che item thất bại | Tách processed/succeeded/refused/failed/cancelled/pending; `partial` có nhãn riêng và manifest mọi item. | Tổng item khớp; xuất không chỉ lấy trang đang xem. |
| Mất dữ liệu khi đóng tab/khởi động lại | Preview có badge “Not saved”; batch submit/import commit/save có thông báo lưu local. Reopen snapshot và Run again là hai hành động khác nhau. | Không hứa tự lưu preview; chạy lại tạo entry mới. |
| Upload bị hiểu là đã lưu hoặc đã huấn luyện | Import ba bước metadata → validation → commit. Dữ liệu lỗi chặn commit; warning cần xác nhận. | Không có auto training/auto merge/auto averaging. |
| Missing bị ngầm thay bằng 0 | Ô `—` đi kèm missing reason; count khớp row report. | Không tạo residual cho missing hoặc endpoint không tương thích. |
| So p-value/xác suất với số đo ΔPSI | Comparison dùng **raw predicted ΔPSI** và observed ΔPSI; ghi residual = predicted − observed. | Units, replicate/aggregation, n và exclusions đều hiện. |
| ClinVar trống bị hiểu là benign | Phân biệt available/no_match/mapping_unavailable/source_unavailable/mapping_conflict. | Không dùng một empty state cho cả năm tình huống. |
| Xóa mất nhiều dữ liệu hơn dự kiến | Dialog liệt kê dependencies và job bị hủy trước confirm; cleanup failure có retry. | Không báo “đã xóa” khi file cleanup chưa xong. |
| Lịch sử thay đổi khi reference được cập nhật | Frozen snapshot label, model/source revision; Run again tạo run mới. | UI không lấy version hiện tại để gắn lại cho run cũ. |

## 4. Khảo sát theme và phong cách trước khi dựng màn hình

Nguồn được mở/kiểm tra ngày 31/10/2026. Đây là tham khảo định hướng, không sao chép nguyên màn hình hoặc coi template bên ngoài là yêu cầu BA.

| Hướng | Nguồn | Điểm phù hợp | Hạn chế | Chọn |
|---|---|---|---|---|
| Workspace tối giản, mật độ vừa | [Linear: A calmer interface](https://linear.app/now/behind-the-latest-design-refresh) | Điều hướng lùi thị giác, phân cấp header/action, dễ tập trung vào công việc | Cần tăng khoảng thở và kích thước mục tiêu so với công cụ cho power user | Nền tảng bố cục |
| Theme theo token, surface phẳng | [Radix Themes](https://www.radix-ui.com/themes/docs/theme/overview) | Tách accent/gray/radius/variant, dễ kiểm soát consistency | Không tự giải quyết ngữ nghĩa dữ liệu khoa học | Nguyên tắc theme |
| Điểm nhấn 3D có chiều sâu | [Spline](https://spline.design/) | Hợp phần giới thiệu/empty state; tạo nhận diện sinh học hiện đại | Không có dữ liệu cấu trúc trong yêu cầu; 3D runtime tạo thêm tải và phụ thuộc | Minh hoạ trừu tượng giới hạn |
| Bộ primitive để dựng Figma | [Figma Simple Design System](https://github.com/figma/sds) | Button/Input/Tab/Tag/Checkbox và spacing có thể tái sử dụng dưới dạng instance | Chưa có domain banner, heatmap, coverage/import states chuyên biệt | Chọn làm thư viện primitive |

**Hướng đề xuất:** workspace sáng, nền gần trắng, ink tối, accent teal, viền mảnh, khoảng cách đều; sidebar ít nhiễu; typography rõ và số tabular. Dùng khối/ribbon có shading tạo cảm giác 3D trong hero, chú thích rõ là minh hoạ trừu tượng, không phải cấu trúc protein được suy luận. Màn hình dữ liệu giữ phẳng. Có bản dark và fallback 360 px theo BA.

Không chọn glassmorphism cho bảng/số liệu do khó giữ tương phản trên nền phức tạp. Không dùng neon/3D cho domain, score hoặc clinical classification. Màu thương hiệu teal **không thay** thang đo BA: probability dùng reversed Viridis, raw score dùng PuOr với tâm 0.

Nguồn tham khảo chỉ dùng ý tưởng bố cục/theme; artwork ribbon là SVG tự dựng, không lấy hình cấu trúc của tác giả khác. Lucide SVG được tải từ kho chính thức, giữ giấy phép ISC/MIT trong `assets/`. Chi tiết nguồn và hash tài liệu trong `sources.json`.

## 5. Kiến trúc thông tin

Navigation chính: **Projects → New analysis → Model → Data & sources**. Jobs và Experimental datasets nằm trong project; kết quả có tab Matrix / Ranking / Compare / Annotations. Không thêm module quản trị vì không có actor quản trị riêng.

| Nhóm giao diện | Trách nhiệm | UC |
|---|---|---|
| Project list / workspace | Tạo/đổi tên dự án; history, jobs, datasets; reopen snapshot | 10 |
| New analysis | Single peptide / peptide batch / whole protein; chọn project khi cần lưu job | 01,04,08 |
| Protein explorer / preview | Search reference; tile map + list; coverage + gaps; chọn tile hoặc submit protein | 04,08 |
| Job progress / outcomes | Pending/running/recovery/cancel và terminal results; mở một tile | 08 |
| Result / ranking / detail | Domain/evidence trước heatmap, shortlist, provenance, export/save | 01,02,03,07,10 |
| Annotation panel | ClinVar/UniProt/GPS; mapping/source/review/conflict; nguồn và disclaimer | 06 |
| Import wizard / dataset | Metadata, validation, warning acknowledgement, immutable commit/revision | 09 |
| Comparison | Dataset/replicate hoặc aggregation rõ; matched counts, raw ΔPSI, missing và incompatible | 05 |
| Model / sources | Event, assay/domain, benchmark limits, hash/version/licence và nguồn không dùng | 07 |
| Dialogs / error states | Create/rename/save/delete/override/cancel, expired preview, failed export/service | 01,03,08,09,10 |

Single preview không bị ép tạo project. Batch/protein bắt buộc chọn project trước submit. Route chỉ chứa ID/accession/index, không chứa sequence/measurement.

## 6. Các luồng tương tác

**A — Peptide đơn:** New analysis → nhập/validate 28 aa → predict → domain gate → result → chọn cell/shortlist → export hoặc Save to project. Với custom peptide chưa ánh xạ: domain unknown và ClinVar mapping unavailable. Khi out: chọn tile khác hoặc explicit warned override; banner đỏ đi cùng result/export.

**B — Protein:** tìm accession → explorer → chọn tile hoặc whole-protein preview → xem coverage/gaps/limits/project/persistence → submit → job → mở kết quả tile. Full windows step 23, không pad/end-align. A6NMZ7 2.263 aa tạo 98 tile; tile 98 là 2.232–2.259, khoảng cuối không phủ 2.260–2.263. Đây là hệ quả công thức BA, không phải nhãn sinh học mới.

**C — Batch:** paste list/multi-FASTA → preview stable input IDs và lỗi từng item → sửa blocking input → xác nhận lưu local → submit → running → completed/partial/failed/cancelled. Cancel giữ completed snapshots, không hứa khôi phục item đã hủy. Sau restart mở cùng job ID; không dùng nút submit mới để “resume”.

**D — Import/compare:** project → import CSV/TSV + assay/units/source/replicate → staged preview → sửa duplicate/WT/nonfinite/coordinate errors → preview lại → acknowledge warnings → commit revision → chọn saved analysis + dataset + replicate → raw ΔPSI comparison hoặc separate endpoint view. Sửa file tạo preview/revision mới; không chỉnh dữ liệu đã commit.

**E — History/delete:** project → reopen frozen snapshot → inspect provenance → Run again tạo entry mới hoặc export snapshot. Delete hiển thị dependency summary → confirm → pending cleanup → success/error retry.

## 7. Quy tắc thị giác và component

| Thành phần | Quy ước |
|---|---|
| Typography | Đề xuất Roboto cho UI vì có trong fallback stack hiện tại; Roboto Mono cho sequence/coordinates/hash. Đây là quyết định thiết kế mới, không nói app hiện tại luôn render Roboto. |
| Type scale | Display 40/48; page title 28/36; section 20/28; body 14/20 hoặc 16/24; caption 12/16. |
| Spacing | Dùng các token SDS 8/16/24 và token cần bổ sung; content padding desktop 32; card radius 12, control radius 8. |
| Actions | Một CTA chính theo bước; hành động hủy/xóa có tên cụ thể, không chỉ icon. |
| Domain | Icon/pattern + chữ + nguồn bằng chứng; status không chỉ dựa màu. |
| Matrix | Đúng 28 hàng × 20 cột, 28 WT masked, 532 cells. Tọa độ tile/protein phân biệt; số liệu focus/tooltip/table đồng bộ. |
| Probability | Header/legend có sự kiện; low → high được gắn giá trị; reversed Viridis. |
| Raw score | PuOr quanh 0, giữ dấu; không gắn `%`. |
| Annotation | Clinical classification không dùng cùng encoding với score; có review/conflict/source state. |
| Comparison | Raw predicted ΔPSI và observation có units; residual cùng units; n/exclusions/aggregation bắt buộc. |
| 3D/motion | SVG trừu tượng chỉnh sửa được; không tự chuyển động; tôn trọng reduced motion khi triển khai. |

Primitive ưu tiên instance của SDS; những thành phần chuyên biệt lặp lại được tạo component local: AppShell/navigation, domain/evidence banner, stat, table header/row, sequence strip, job status/progress và dialog. Token có scope và WEB code syntax. Typography brand được override có chủ đích lên Roboto; giữ instance/reference của primitive.

## 8. Trạng thái và nội dung bắt buộc

| Bề mặt | Trạng thái thiết kế cần có |
|---|---|
| Input/search | empty, typing/valid, invalid alphabet/length, searching, no match, unavailable |
| Domain | measured/predicted in/out; borderline; unknown; unreliable; explicit override |
| Result | loading/cancel, success/warning, refused, empty ranking, export failure/retry, snapshot unavailable |
| Annotation | available, no match, mapping unavailable, source unavailable, mapping conflict |
| Job | pending, running, recovery, completed, partial, failed, cancelled; cancel requested |
| Import | staged, blocking errors, committable + warnings, commit pending/success/error, preview expired |
| Comparison | compatible matched, missing/unmatched, incompatible endpoint, undefined metric, dataset absent |
| Persistence/delete | unsaved, save pending/success/error, frozen snapshot, dependencies/confirm, cleanup pending/error/retry |

Các trạng thái dùng chung được trình bày trong board component/state; không biến mỗi biến thể API thành một route mới. Prototype nối các bước tiêu biểu; Figma không thực thi inference, upload, lưu/xóa dữ liệu hay job worker.

## 9. Responsive và accessibility

- Desktop 1440 px là màn hình làm việc chính. Sidebar cố định, content co giãn; dữ liệu không bị đè lên nhau khi đổi label.
- 360 px: header gọn, navigation menu, warning/evidence vẫn đứng trước score; mặc định bảng ranking. Matrix là lựa chọn có horizontal scroll, không thu 20 cột đến mức không đọc được.
- Control target tối thiểu 44 px; icon có tên; tab/focus rõ. Matrix dùng roving focus; arrow keys, Enter chọn, Esc thoát; có table thay thế.
- Text thường mục tiêu 4.5:1, chữ lớn/controls 3:1. Có kiểm tra token chính; không gọi đó là audit WCAG đầy đủ.
- Staged/committed, missing/zero, no_match/unavailable đều bằng chữ. Không đặt cảnh báo trong tooltip duy nhất.
- Thông báo progress dùng polite live region; lỗi trường gắn label/description và đưa focus tới trường cần sửa khi triển khai.

## 10. Handoff và đánh giá tiếp theo

`figma-manifest.json` lưu file/session/page/frame IDs, component/token inventory, fixture label và kiểm tra cấu trúc/ảnh. `screen-map.json` liên kết screen → UC/FR/test; `sources.json` giữ nguồn tham khảo và hash tài liệu đã đọc. `scripts/` chứa mã dựng Figma; đây là công cụ tạo thiết kế, không sửa runtime app.

Trước triển khai cần review wording sinh học với GVHD, test task với người dùng nghiên cứu và chốt các ngưỡng cấu hình bằng đo local. Đề xuất task test: chọn 3 phép thay thế và giải thích sự kiện xác suất; tìm terminal gap; phân biệt job partial; sửa duplicate import; giải thích vì sao metric bị khóa khi khác assay; mở lại đúng snapshot. Ghi completion/error/diễn giải sai và thời gian thực tế, **không bịa số người hay tỷ lệ thành công**.

Phần review cục bộ đã kiểm tra: đủ UC-01–10 trong danh mục, matrix/WT đúng, không có lỗi console/overflow ở node spec, hotspot có đích, luồng custom không tự ánh xạ và nút có chiều cao 44 px. Xem [kết quả kiểm tra](review-validation.json) và [ảnh](previews/df09.png). Kiểm tra này không thay thế kiểm tra native Figma, keyboard/assistive technology đầy đủ hay runtime app.

Phần Figma hoàn tất khi các màn hình đã thực sự nhập, primitive/instances và layer chỉnh sửa được đã đọc lại, và ảnh Figma đã review. Trạng thái hiện tại **chưa đạt bước này do quota**. Việc import và đối chiếu native vẫn chờ. Các kiểm tra runtime, R3 integration, browser/a11y và nghiệm thu khoa học thuộc bước triển khai riêng.
