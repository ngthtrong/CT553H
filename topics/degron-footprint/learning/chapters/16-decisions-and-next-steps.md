# Tổng hợp: đã làm được gì và vì sao đi tiếp theo hướng này?

## Đóng góp cần nhìn theo chuỗi bằng chứng

Giá trị đề tài hiện nằm ở một chuỗi: xác định endpoint có nhãn → dựng và kiểm ΔPSI → chia nhóm hạn chế rò rỉ → đối chứng từ đơn giản tới pLM/head → phân tích theo miền → thiết kế công cụ giữ nguồn gốc. Chưa cần tuyên bố kiến trúc hoàn toàn mới để thấy giá trị của kiểm soát và đánh giá có hệ thống.

| Quyết định | Căn cứ đã có | Hệ quả/hướng tiếp tục |
|:--|:--|:--|
| Tập trung mutation ΔPSI | Có saturation/scanning và quy tắc WT kiểm được | Giữ suy luận ở reporter/assay, không gán E3 |
| Giữ Ridge mạnh | Baseline ổn định, W5 có lợi ở R6 | Mọi head lớn cần đối chứng cùng dữ liệu |
| Mở full-PSI | D/E giảm MAE so B | Báo thêm tầng PSI và guardrail |
| Kiểm head ngữ cảnh | CNN-D cải thiện so pointwise-D trong run | Tiếp tục kiểm dung lượng/budget và ensemble |
| Chuyển giao scanning | Có lợi hơn scratch trong v3 đã lưu | Giữ endpoint và chia nhóm nguồn chặt |
| Khảo sát local có giới hạn | Cần so biểu diễn và tuning trong runtime khớp | Đủ fold/seed, OOF và CI trước kết luận |
| Chưa thay serving model | Chưa đủ export/promotion/kiểm miền mới | Giữ artifact baseline tới quyết định riêng |

Các hàng trên là tổng hợp [NC-01–NC-17; KH-01–KH-03; PM-01], không phải bảy lần xác nhận độc lập.

## Những giả thuyết đã bị thu hẹp

“Nhiều dữ liệu hơn luôn tốt” được thay bằng “dữ liệu nào, endpoint nào, trọng số nào?”. P3 tile-label không chứng minh lợi ích chuyển giao; trộn nhãn có trọng số cũng không thắng mặc định. “Model lớn hơn luôn tốt” được thay bằng phép so có head, cohort và CI. “Score cao là đáng tin” được thay bằng kiểm calibration và miền sử dụng.

Kết quả âm giữ vai trò thực tế: ngăn lặp lại một hướng không có căn cứ trong thiết kế hiện tại và giúp chọn câu hỏi chính xác hơn. Không được bỏ các run thất bại, resource-blocked hoặc kết quả kém chỉ vì chúng làm bảng khó đẹp.

## Trật tự công việc tiếp theo

1. **Hoàn tất development local theo plan:** giữ identity, preflight model, đủ fold/seed và artifact; không đổi protocol giữa chừng để chạy vừa.
2. **Collect và kiểm số:** row coverage, cohort chung, OOF, ensemble, CI, strata và guardrail; tách metric trung bình seed với ensemble.
3. **Khóa lựa chọn và kiểm held-source:** giữ recipe T đã chỉ định, công bố lịch sử nguồn; không dùng T chọn model.
4. **Hoàn tất calibration/export phù hợp:** xác suất, model card và inference package cùng phiên bản; có kiểm số qua đường suy luận độc lập.
5. **Tích hợp phần mềm theo phạm vi local:** đúng gate R3, lưu bền, jobs, import, annotation, recovery; đo hiệu năng thực tế.
6. **Cập nhật luận văn theo bằng chứng:** bổ sung kết quả đủ, phương pháp và giới hạn, để các phần chưa có dữ liệu ở trạng thái pending có lý do.

Đây là thứ tự phụ thuộc logic. Một số việc tài liệu/giao diện có thể làm song song, nhưng không cần chờ training để sửa một lỗi provenance; cũng không dùng giao diện hoàn thiện để bỏ qua việc đánh giá model.

## Tái lập cần ba loại “đúng”

**Đúng dữ liệu:** nguồn/phiên bản/hash, mapping, QC, nhãn, fold. **Đúng thực thi:** code/runtime/weights, seed, trạng thái artifact và resume. **Đúng diễn giải:** metric, population, uncertainty, leakage và giới hạn. Build PDF thành công chỉ xác nhận tài liệu được dựng, không xác nhận cả ba loại đúng của nghiên cứu.

**Manifest** là bản kê machine-readable giữ liên kết các thành phần. **Data identity** phân biệt bundle dữ liệu; **campaign identity** còn phụ thuộc protocol/code/runtime liên quan. Không sửa hash trong manifest để làm checkpoint khác phiên bản có vẻ hợp lệ. Hash chứng minh cùng byte, không tự chứng minh dữ liệu có ý nghĩa sinh học đúng.

## Những điều vẫn chưa biết

Chưa có bằng chứng trong sách cho hiệu năng local cuối, khả năng mọi pLM vượt baseline, calibration của mọi head full-PSI, tính khái quát của protein nguyên vẹn hay tác động bệnh lý. Chưa có nghiệm thu đầy đủ workspace mới. Nguồn mới/structure thiếu input phải ghi pending; dữ liệu giả không lấp được khoảng trống đó.

::: {.exercise title="Tự kiểm 16"}
1. Nêu một kết quả dương, một kết quả âm và quyết định mà mỗi kết quả hỗ trợ.
2. Vì sao manifest đúng chưa đủ xác nhận kết luận khoa học?
3. Công việc nào cần xong trước khi gọi model mới là model đang phục vụ?
:::
