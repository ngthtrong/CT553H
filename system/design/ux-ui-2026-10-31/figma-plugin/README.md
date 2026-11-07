# Nhập thiết kế bằng native development plugin

**Giới hạn đã gặp:** Figma MCP báo hết quota Starter trong phiên 31/10/2026. File Figma đã có nền tảng; các màn hình chưa được ghi. Gói này là phương án nhập thủ công các layer từ bản review, không gọi MCP, không có network access và chưa được chạy/kiểm tra trong Figma native.

1. Mở Figma Desktop và tạo một development plugin cho Figma Design. Giữ `manifest.json` có **ID do Figma cấp**. Không nhập trực tiếp `manifest.template.json` khi còn placeholder.
2. Chạy lệnh dưới đây, thay đường dẫn bằng manifest vừa được Figma tạo:

   ```bash
   python3 scripts/configure_plugin.py /path/to/figma-created/manifest.json
   ```

   Hoặc chép `figma-plugin/code.js` vào thư mục plugin vừa tạo; đặt `main` thành `code.js`, `documentAccess` thành `dynamic-page`, `editorType` thành `["figma"]`, network allowed domains thành `["none"]`. Giữ nguyên ID thật của manifest.

3. Mở [file thiết kế](https://www.figma.com/design/MdMLYZQfXqGcL3br3JMunM), chạy development plugin, bấm **Build editable screens** một lần. Chờ thông báo hoàn tất.
4. Review các trang Direction & UX, Research workspace và Components & states. Đối chiếu font, wrapping, overrides, matrix và prototype links với `review.html`.

Plugin tạo text, vector, auto-layout frames, semantic colour/spacing tokens, reusable components/instances và liên kết prototype. Artwork SVG là đối tượng nội dung riêng; toàn bộ UI không bị chuyển thành một ảnh nền. Plugin dựng component local từ node spec đã review; việc tái sử dụng primitive SDS trong các màn hình native chưa được xác minh.

Mỗi lần chạy đặt tên frame theo run ID; không ghi đè frame có sẵn. Chạy lại sẽ tạo thêm một bản, vì vậy chỉ retry sau khi xem thông báo và kiểm tra phần import trước. Nếu import dừng, không suy ra các frame còn lại đã hoàn tất. Đảm bảo bạn có quyền chỉnh sửa Design file và Roboto/Roboto Mono khả dụng.

ID manifest là do Figma cấp; đây là bước cấu hình development plugin, không phải API key. Tham khảo [Create a classic plugin for development](https://help.figma.com/hc/en-us/articles/360042786733-Create-a-classic-plugin-for-development) và [Plugin Manifest](https://developers.figma.com/docs/plugins/manifest/).
