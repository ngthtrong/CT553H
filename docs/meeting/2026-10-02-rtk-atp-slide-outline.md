# Dàn ý và kịch bản trình bày — buổi gặp GVHD 02/10/2026

> Bản dùng để nói, không phải để đọc nguyên văn. Deck: https://claude.ai/artifact/GGw1vJ2wpJKF63gmoBgLYT · mã nguồn: [session-01-slides/](session-01-slides/) · thuyết minh đầy đủ: [topic-proposal.md](../topics/rtk-atp-applicability/04-proposal/topic-proposal.md).
>
> 13 slide. Nếu được 10 phút: nói slide 1–6 và 10–13, nhắc nhanh 7–9. Nếu được 5 phút: slide 1, 2, 5, 7, 11, 13.

## Nguyên tắc xuyên suốt buổi nói

1. **Mở đầu bằng mục tiêu, không bằng phê bình.** Câu mở: *“Em muốn đo điều kiện mà truy hồi thật sự hữu ích, rồi biến kết quả đó thành cảnh báo miền áp dụng cho người dùng.”* **Không** mở đầu bằng “bài cũ bị rò rỉ”.
2. **Nói “kiểm soát rò rỉ”**, không nói “chống rò rỉ” hay “không rò rỉ”. Lý do nói ra được: PLM có thể đã gặp các chuỗi này khi tiền huấn luyện.
3. **Mọi con số đều phải có nguồn.** Số dữ liệu là số tự đếm từ tệp đã tải. Số của bài báo thì nói rõ là của bài báo.
4. **Nhận xét mã nguồn luôn kèm giới hạn.** “Đây là đặc điểm của mã công khai em đã đọc; em chưa kết luận nó tạo ra mọi con số trong bài.”
5. **Không có kết quả mô hình nào.** Chưa trích embedding, chưa huấn luyện, chưa chạy alignment.

## Mạch 13 slide

| # | Slide | Thông điệp duy nhất của slide | Điều phải nói ra miệng |
|---:|---|---|---|
| 1 | `cover` | Đề tài đã chọn, đã có dữ liệu | Câu mở đầu ở nguyên tắc 1; “một người, 14 tuần, dữ liệu đã tải và đếm xong” |
| 2 | `scope` | Phân loại nhị phân ở mức residue | Đọc bảng ví dụ; rồi đọc danh sách “không làm” để chặn câu hỏi ngoài phạm vi |
| 3 | `pipeline` | Truy hồi ở đây là bổ sung đặc trưng, không phải chatbot | k = 5 ở mức residue, trộn 1:1; chỗ phải sửa là giữ mã protein và vị trí residue trong index |
| 4 | `data` | Mọi số là số em tự đếm | Snapshot kho RAG **không kèm tệp nhãn** dù README ghi 2.676 dương; **chưa chạy alignment** |
| 5 | `leakage` | Bốn loại rò rỉ, mỗi loại kiểm soát khác nhau | Đồng dạng trong kho **chưa chắc** là rò rỉ nếu kho có sẵn khi triển khai |
| 6 | `protocol` | Chín bước, khóa theo thứ tự | Bước 6 khóa cấu hình, bước 8 chấm test một lần, bước 9 bootstrap theo protein |
| 7 | `rq1` | Truy hồi giúp bao nhiêu, khi đã kiểm soát đồng dạng | Nhánh C (k-NN) là nhánh không được cắt |
| 8 | `rq2` | Identity có dùng được làm tín hiệu miền áp dụng không | Gọi là **tín hiệu miền áp dụng**, chưa gọi là “độ tin cậy” |
| 9 | `metrics` | Dương 0,96% nên AUPRC là chính | Accuracy không dùng làm kết luận |
| 10 | `product` | Người dùng thấy dự đoán **và** vùng dữ liệu nó đứng trên | Cảnh báo là RQ2 hiện ra thành tính năng, không phải giao diện trang trí |
| 11 | `contributions` | Ba đóng góp, không cần kiến trúc mới | Tự nêu rủi ro “chấm lại bài của thầy” trước khi thầy nghĩ tới |
| 12 | `plan` | Sáu giai đoạn, mỗi giai đoạn một cổng dừng | Thứ tự bất biến: khóa split → khóa cấu hình → mở test → hoàn thiện hệ thống |
| 13 | `questions-for-advisor` | Sáu câu cần câu trả lời | Câu 1 và 2 là hai câu quan trọng nhất; ghi lại câu trả lời ngay trong buổi |

## Câu hỏi dễ gặp và cách trả lời

**“Mới ở đâu, khi RTK_RAG đã làm bài toán này?”**
> “Em không đề xuất kiến trúc mới. Em đo **điều kiện** mà truy hồi hữu ích: sau khi gom cụm theo đồng dạng và tách kho truy hồi, lợi ích còn lại bao nhiêu, và có đến từ MCNN hay chỉ từ việc protein giống nhau. Phần đó em có nhánh k-NN để tách ra. Kết quả của câu hỏi đó thành một tính năng cảnh báo cho người dùng.”

**“Em định phê bình bài của nhóm thầy à?”**
> “Không ạ. Em dùng việc đọc mã để thiết kế giao thức của chính em cho chặt, và để biết chỗ nào em phải hỏi lại thầy. Chỗ em đọc được trong mã công khai em có ghi kèm giới hạn, vì notebook thiếu module nạp dữ liệu nên em chưa thể nói đó là phiên bản tạo ra số liệu trong bài.”

**“Nếu truy hồi không giúp thì sao?”**
> “Đó vẫn là câu trả lời cho RQ1 và em sẽ báo đúng như vậy, kèm khoảng tin cậy. Khi đó em dồn sức vào RQ2 và hệ thống. Em muốn xin thầy xác nhận trước là một kết quả âm có kiểm soát thì được chấp nhận.”

**“Sao không dùng cả 69 RTK làm independent test như bài gốc?”**
> “Vì em cần một phần RTK để quét và khóa ngưỡng cảnh báo. Nếu em chọn ngưỡng trên chính tập em chấm thì test không còn độc lập. Nên em tách RTK-development và RTK-test, và chấp nhận test nhỏ hơn với khoảng tin cậy rộng hơn.”

**“14 tuần một người có làm nổi không?”**
> “Em thu từ ba RQ xuống hai. Em bỏ việc so cùng lúc CD-HIT 30 với 40, nhiều loại kho, nhiều alpha và nhiều k. Phần kiểm toán ngưỡng em hạ thành thí nghiệm phụ. Mỗi giai đoạn có cổng dừng, và cổng tuần 1–2 là có được manifest split khóa được.”

**“AUPRC là gì, sao không dùng accuracy?”**
> “Tập RTK có 711 residue dương trên 73.270 âm, khoảng 0,96%. Một mô hình luôn dự đoán âm vẫn đạt accuracy trên 99%. AUPRC nhìn vào precision và recall của lớp dương nên phân biệt được các mô hình.”

## Việc phải làm trước khi vào buổi

- [ ] Điền tên và MSSV vào slide bìa (đang là `[Họ tên sinh viên]` / `[MSSV]`).
- [ ] Tự mở deck một lượt trên claude.ai, xem có chỗ nào tràn hoặc xuống dòng xấu.
- [ ] Mở sẵn `Dataset/rag_prottrans_GPU.py` và hàm `model_test` trong `CODE/MCNN_npy.ipynb`, để nếu thầy hỏi thì chỉ đúng dòng.
- [ ] Mở sẵn [báo cáo dữ liệu](../topics/rtk-atp-applicability/03-data/data-report.md) để tra số khi bị hỏi.
- [ ] Giấy bút ghi câu trả lời của thầy cho sáu câu ở slide 13.

## Ghi ngay sau buổi

Tạo `session-01-minutes.md` với: thầy chọn/sửa gì trong phạm vi, câu trả lời cho sáu câu, tài nguyên thầy cho dùng (trọng số, embedding, GPU, nhãn kho RAG), và việc thầy yêu cầu làm trước buổi sau.
