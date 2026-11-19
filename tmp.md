# Quy trình vẽ sơ đồ học thuật cho CT553H

Với luận văn CT553H, ưu tiên **TikZ** cho sơ đồ phương pháp và kiến trúc cần đồng bộ với LaTeX, **draw.io Desktop** cho sơ đồ cần chỉnh trực tiếp, và **Matplotlib** cho hình lấy số liệu từ kết quả thí nghiệm. [Quy ước tài sản của luận văn](report/assets/README.md)

## 1. Chọn công cụ và ký pháp

| Nội dung | Công cụ | Quy ước cần thể hiện |
| --- | --- | --- |
| Pipeline nghiên cứu, xử lý dữ liệu, thiết kế thí nghiệm | draw.io để chỉnh trực tiếp, Mermaid để lưu nguồn văn bản trong Git, TikZ để dùng chung phông và ký hiệu LaTeX | Thể hiện đầu vào, đầu ra và điều kiện rẽ nhánh. Với đánh giá ML, chỉ rõ tập dùng để chọn mô hình, tập dùng để đánh giá và tập giữ riêng nếu có. [draw.io](https://www.drawio.com/docs/manual/mermaid/) · [Mermaid](https://mermaid.js.org/intro/) · [PGF/TikZ](https://ctan.org/pkg/pgf) |
| Kiến trúc phần mềm, sequence, trạng thái, ERD | draw.io, PlantUML hoặc Mermaid | Dùng C4 cho góc nhìn kiến trúc, UML cho sequence và trạng thái, Crow’s Foot cho ERD. Ghi ý nghĩa mũi tên, điều kiện chuyển trạng thái hoặc bội số quan hệ tùy loại hình. [C4](https://c4model.com/diagrams/notation) · [OMG UML](https://www.omg.org/spec/UML/2.5.1) · [PlantUML](https://plantuml.com/) |
| Sàng lọc tài liệu trong tổng quan hệ thống | Mẫu Word PRISMA 2020 hoặc gói PRISMA2020 của R | Chọn mẫu theo loại tổng quan và nguồn tìm kiếm, đối chiếu số bản ghi qua từng bước và ghi lý do loại ở bước đánh giá toàn văn. [Mẫu PRISMA](https://www.prisma-statement.org/prisma-2020-flow-diagram) · [Gói R](https://cran.r-project.org/package=PRISMA2020) |
| Minh họa khái niệm sinh học, ghép nhiều panel | Inkscape để chỉnh vector, BioRender để dựng từ thư viện, SciDraw hoặc NIH BioArt Source để tìm hình thành phần | Kiểm giấy phép từng tài sản và ghi nguồn khi cần. Với BioRender, kiểm quyền xuất bản theo gói trước khi đưa hình vào luận văn công khai hoặc bài báo. [Inkscape](https://inkscape.org/about/) · [BioRender](https://www.biorender.com/academic-license) · [SciDraw](https://scidraw.io/licensing) · [NIH BioArt](https://bioart.niaid.nih.gov/faqs) |
| Đồ thị kết quả, khoảng tin cậy, so sánh mô hình | Matplotlib hoặc ggplot2 | Sinh hình từ dữ liệu bằng script. Ghi đơn vị, cỡ mẫu hoặc đơn vị phân tích, và ý nghĩa khoảng sai số. [Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html) · [ggplot2](https://ggplot2.tidyverse.org/reference/ggsave.html) |

## 2. Quy trình vẽ và kiểm tra

1. **Chốt một thông điệp cho mỗi hình.** Ví dụ với sơ đồ nested evaluation, mọi quyết định chọn mô hình diễn ra trong các nhóm huấn luyện của outer fold. Đối chiếu từng bước với protocol hoặc mã nguồn và từng số liệu với tệp kết quả. Đưa phần giải thích dài vào chú thích. [Ten Simple Rules for Better Figures](https://doi.org/10.1371/journal.pcbi.1003833)
2. **Vẽ luồng chính rồi thêm nhánh.** Chọn một hướng đọc, căn các hộp theo hàng hoặc cột, ghi điều kiện cạnh mũi tên và giảm đường cắt nhau. Dùng nhãn hoặc kiểu nét cùng với màu để bản in đen trắng vẫn diễn giải được. Với nhiều panel, dùng nhãn `a`, `b`, `c` và dẫn theo cùng thứ tự trong chú thích. [C4 notation](https://c4model.com/diagrams/notation) · [Nature Figure Guide](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/)
3. **Lưu bản chỉnh sửa và xuất hình.** Giữ nguồn `.drawio`, `.mmd`, `.tex` hoặc script cùng dữ liệu đầu vào theo quy ước repo. Với Mermaid trong draw.io, dùng **Arrange → Insert → Mermaid**, chọn **Diagram** để chỉnh từng hộp và mũi tên, lưu `.drawio`, rồi xuất PDF vector đã cắt sát hình để chèn vào XeLaTeX. Có thể dùng PNG để xem trước. [Nhập Mermaid](https://www.drawio.com/docs/manual/mermaid/) · [Xuất hình từ draw.io](https://www.drawio.com/docs/manual/export/export-diagram/) · [Định dạng hình trong repo](report/assets/README.md)
4. **Chèn và xem lại trong PDF luận văn.** Kiểm chữ, nét và chú giải ở chiều rộng thực tế, thử bản xám, rồi kiểm trang chứa hình và các trang kề trên bản một mặt và hai mặt nếu bố cục thay đổi. Đặt chú thích dưới hình, `\label` ngay sau `\caption`, và dẫn hình bằng `Figure~\ref{fig:...}`. Khi gửi bài báo, dùng thông số kích thước, phông và định dạng của nơi nhận bài. [Quy tắc CT553H](CLAUDE.md#quy-tắc-bố-cục-và-đánh-số-của-report--07112026) · [Ví dụ thông số của Nature](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)

## 3. Skill và mẹo từ cộng đồng

- **`drawio-skill` của Agents365-ai.** Skill đã có trong repo. Dùng để dựng sơ đồ `.drawio`, chạy `validate.py --score` để kiểm cấu trúc, rồi xuất PNG xem trước và PDF để chèn. Đối chiếu thêm ngữ nghĩa của mỗi mũi tên với protocol hoặc mã nguồn. [Skill trong repo](.agents/skills/drawio-skill/SKILL.md) · [GitHub](https://github.com/Agents365-ai/drawio-skill)
- **`scientific-visualization` của K-Dense.** Tham khảo khi cần chọn bảng màu, biểu diễn độ bất định và xuất hoặc rà hình từ Matplotlib. [Skill trên GitHub](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-visualization/SKILL.md)
- **`scientific-figure-skills` của enesgul23.** Tham khảo quy trình lập kế hoạch, dựng, rà soát và đóng gói hình nhiều panel có thể tái tạo. [Skill trên GitHub](https://github.com/enesgul23/scientific-figure-skills)
- **Học cách căn chỉnh từ ví dụ có mã nguồn.** TeXample có mẫu TikZ về bố trí nút và đường nối. Nhóm tác giả *Ten Simple Rules* công khai script minh họa cách sinh hình bằng Matplotlib. [TeXample](https://texample.net/) · [Script của bài PLOS](https://github.com/rougier/ten-rules)
- **Kiểm màu ở điều kiện đọc thật.** ColorBrewer có bộ lọc cho người khó phân biệt màu và cho bản in. Kiểm tiếp bản xám của hình hoàn chỉnh để chắc các nhóm vẫn phân biệt được qua nhãn, ký hiệu hoặc kiểu nét. [ColorBrewer](https://colorbrewer2.org/) · [Nature Figure Guide](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/)

## 4. Mẫu có sẵn trong CT553H

- **Nested evaluation hiện hành.** Sơ đồ TikZ đã cập nhật theo protocol refit và dùng bộ style chung của luận văn. [Nguồn sơ đồ](report/assets/figures/nested-evaluation.tex) · [Style TikZ](report/assets/figures/style.tex) · [Chú thích và cách chèn](report/chapters/sections/campaign-methods.tex)
- **Sơ đồ draw.io ngày 06/11.** Có nguồn chỉnh sửa, PDF vector, PNG xem trước và lệnh xuất. Phiên bản nested evaluation tại đây là snapshot trước đợt refit. [Bộ sơ đồ campaign](report/assets/diagrams/campaign-2026-11-06/README.md)
- **Hình kết quả sinh từ script.** Ví dụ tạo đồ thị ngân sách và recall từ kết quả đánh giá đã lưu. [Script sinh hình](report/assets/ch4/build_prioritization_assets.py)

## 5. Thiết kế giao diện web với ChatGPT/Codex và Claude

Với frontend CT553H đã có prototype và design tokens, ưu tiên **Impeccable** để góp ý thiết kế và **Playwright** để kiểm giao diện trong trình duyệt. Với landing page mới, dùng **`frontend-app-builder`** của OpenAI hoặc **`frontend-design`** của Anthropic để chốt hướng hình ảnh trước khi triển khai. [Workspace UI v2](system/design/workspace-ui-v2/README.md) · [Tokens frontend](system/app/frontend/src/styles/tokens.css)

### Skill và công cụ thay thế UI UX Pro Max

| Skill hoặc công cụ | Dùng khi nào | Cách giao việc cho agent |
| --- | --- | --- |
| **Impeccable** · Codex, Claude Code | UI đã có nhưng bố cục, typography hoặc mật độ thông tin cần cải thiện | Dùng `critique` để xếp hạng vấn đề thiết kế, `audit` để rà responsive và accessibility. Giao sửa các điểm có ảnh hưởng lớn nhất. Ví dụ `$impeccable critique` trong Codex hoặc `/impeccable critique` trong Claude Code. [Tài liệu](https://github.com/pbakaus/impeccable) |
| **`frontend-app-builder`** · OpenAI Codex | Làm trang mới từ brief hoặc mockup | Dựng concept cho màn hình chính, xác định tokens và component, rồi đối chiếu ảnh chụp bản chạy với concept. [Skill](https://github.com/openai/plugins/blob/main/plugins/build-web-apps/skills/frontend-app-builder/SKILL.md) |
| **`frontend-design`** · Anthropic Claude | Muốn agent đề xuất hướng hình ảnh cho website mới | Mô tả người dùng và tác vụ chính, gửi ảnh tham khảo, rồi yêu cầu giải thích lựa chọn typography, bố cục và hình ảnh trước khi triển khai. [Skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) |
| **Taste Skill** · Leonxlnx | Thử nhiều hướng thiết kế cho landing page hoặc redesign | Dùng `design-taste-frontend` với ảnh tham khảo, rồi kiểm bản dựng trong trình duyệt. Có thể giao hai hướng thiết kế cho cùng một nội dung. [GitHub](https://github.com/Leonxlnx/taste-skill) |
| **`web-design-guidelines`** · Vercel | Rà giao diện sau khi triển khai | Giao review một route hoặc nhóm file và yêu cầu trả kết quả theo `file:dòng`, ưu tiên lỗi ảnh hưởng đến bàn phím, biểu mẫu, nội dung hoặc responsive. [Vercel Agent Skills](https://vercel.com/docs/agent-resources/skills) |
| **Figma MCP + `figma-design-to-code`** | Đã có frame Figma cần chuyển thành giao diện chạy được | Gửi link đến đúng frame, yêu cầu agent lấy cả dữ liệu thiết kế và screenshot, rồi ánh xạ chúng sang component và tokens trong repo. [Skill](https://github.com/figma/mcp-server-guide/blob/main/skills/figma-design-to-code/SKILL.md) · [Hướng dẫn Figma](https://help.figma.com/hc/en-us/articles/34855090823063-MCP-server-best-practices) |
| **Playwright** | Cần kiểm responsive, thao tác và trạng thái trên trình duyệt thật | Cho agent mở localhost, thực hiện luồng người dùng, chụp ảnh trước và sau, kiểm bàn phím và chạy axe cho lỗi accessibility tự động phát hiện được. [Playwright cho coding agent](https://playwright.dev/docs/getting-started-cli) · [Kiểm accessibility](https://playwright.dev/docs/accessibility-testing) |

**Claude Design hoặc Artifacts** phù hợp để thử ý tưởng ngay trong chat bằng prototype tương tác. Khi triển khai vào repo, dùng Codex hoặc Claude Code để tận dụng component hiện có và kiểm thử trên localhost. [Claude Design](https://support.claude.com/en/articles/14604416-get-started-with-claude-design) · [Claude Artifacts](https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them) · [Quy trình frontend với Codex](https://learn.chatgpt.com/use-cases/frontend-designs)

### Quy trình và mẹo giao việc

1. **Bắt đầu từ một tác vụ thật.** Với CT553H, dùng luồng chọn một ô trên ma trận, đọc inspector và thêm vào shortlist. Tác vụ này giúp agent xác định phần cần nổi bật và phần có thể thu gọn. [Refactoring UI](https://refactoringui.com/)
2. **Gắn từng ảnh tham khảo với một mục đích.** Chỉ rõ ảnh nào tham khảo mật độ bảng, phân cấp chữ hoặc vị trí inspector. Nếu đã có mockup, gửi cả desktop, mobile và những trạng thái loading, empty hoặc error có ảnh hưởng đến bố cục. [Hướng dẫn của OpenAI](https://learn.chatgpt.com/use-cases/frontend-designs)
3. **Dùng cùng nguồn thiết kế qua các phiên.** Cho agent đọc tài liệu Workspace UI v2 và `tokens.css` trên mỗi tác vụ UI. Nếu cần hướng dẫn chung cho nhiều agent, dùng `DESIGN.md` để ghi typography, màu, khoảng cách và quy tắc component. Skill `design-system` trong repo có hướng dẫn về tokens và trạng thái component. [Workspace UI v2](system/design/workspace-ui-v2/README.md) · [Tokens frontend](system/app/frontend/src/styles/tokens.css) · [Skill trong repo](.agents/skills/design-system/SKILL.md) · [Google Labs về DESIGN.md](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/)
4. **Yêu cầu bằng chứng từ trình duyệt.** So sánh ảnh trước và sau ở desktop và mobile, thử dữ liệu dài, kiểm focus và thao tác bàn phím rồi sửa lỗi nhìn thấy. Frontend CT553H đã khai báo Playwright và axe cho lượt kiểm này. [Cấu hình phụ thuộc frontend](system/app/frontend/package.json) · [Playwright accessibility](https://playwright.dev/docs/accessibility-testing)

### Prompt mẫu cho CT553H

> Đọc `system/design/workspace-ui-v2/README.md` và `system/app/frontend/src/styles/tokens.css`. Rà màn Analysis theo luồng chọn ô trên ma trận, đọc inspector và thêm vào shortlist. Chạy frontend local, chụp màn hình ở 1440 px và 390 px, rồi nêu ba vấn đề lớn nhất về phân cấp thị giác, mật độ hoặc thao tác. Sửa ba điểm đó bằng component và tokens hiện có. Kiểm lại bằng bàn phím và gửi ảnh trước/sau cùng đường dẫn local.
