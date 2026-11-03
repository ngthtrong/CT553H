# Train local đang tiếp diễn: hướng đi và lý do

::: {.roadmap title="Chỉ trình bày thiết kế, không công bố kết quả local"}
Chương này giải thích kế hoạch đã chốt ở mốc 03/11/2026. Nó không báo cáo metric local, thứ hạng pLM, chất lượng checkpoint đang chạy hay kết quả LoRA chưa đủ. Không khởi chạy, dừng hoặc sửa campaign để viết tài liệu học. Nguồn là kế hoạch và protocol, không phải score fit từng phần. [KH-01; KH-02; KH-03]
:::

## Mục tiêu: tách ảnh hưởng họ mô hình và cách thích nghi

Kaggle đã cho bằng chứng development với ESM2-35M. Câu hỏi tiếp theo là frozen feature của các họ/quy mô khác và việc tinh chỉnh có đem lại giá trị trong cùng thiết kế không. Cần head chung, cùng arm B/D, cùng fold và ba seed 17/29/43 để giảm số yếu tố thay đổi.

Kế hoạch local gồm chín checkpoint: ESM2-8M/35M/150M/650M, ESM1b-650M, ESM1v-650M-1, ESMC-300M, ProtT5 encoder và Ankh base. Đây là **danh sách dự kiến khảo sát**, không phải danh sách đã có kết quả so sánh hoàn chỉnh. Quy mô lớn hơn tốn tài nguyên hơn nhưng không bảo đảm tốt hơn cho peptide ngắn hoặc ΔPSI. [KH-01]

## Bước 1: preflight trước khi chi ngân sách train

**Preflight** là kiểm nhanh khả năng dùng đúng model trên runtime hiện có: tokenizer có giữ đúng 28 residue không; có token đặc biệt nào; vector có đúng chiều, hữu hạn và ổn định khi lặp lại không; peak VRAM và thời gian forward thế nào. Một tensor toàn NaN không được chuyển thành feature rồi tiếp tục train.

**VRAM** là bộ nhớ GPU; nó phải chứa weights, activation và phần bộ nhớ khác tùy tác vụ. Frozen extraction không cần lưu gradient như tuning, nhưng model lớn vẫn có thể quá bộ nhớ. GPU nhiều card không tự cộng VRAM nếu runner chưa hỗ trợ chia model. Model resource-blocked/tokenizer-blocked phải được ghi lý do; không tự đổi kiến trúc, quantization hoặc điểm cắt dữ liệu để ép chạy. [KH-02]

Runtime của kế hoạch được ghim theo Python, Torch/CUDA, thiết bị, code và weights. Thay một thành phần có thể đổi số học và campaign identity. Không cài requirements CPU/historical đè vào môi trường CUDA đang dùng. Hướng này bảo vệ khả năng đối chiếu, không nhằm tuyên bố một runtime luôn tốt nhất.

## Bước 2: frozen feature với đầu Ridge/PCA chung

Đầu tiên trích feature mà không cập nhật backbone, lưu các shard theo row ID, revision và dtype. Feature được lưu float16 để giảm dung lượng; phép fit/head theo quy định riêng. Không hiểu “file float16” thành “mọi bước tính đều float16”. PCA64 chỉ fit train; context W5 được giữ riêng trong pipeline tương ứng. [KH-02; KH-03]

**Shard** là một phần của tập feature; **checksum/hash** giúp kiểm byte nội dung và phát hiện nhầm phiên bản. Khi ghép, cần không trùng row, không thiếu row và cùng data identity. Feature nhanh nhưng lệch thứ tự mutation key sẽ cho kết quả sai rất khó phát hiện.

Lý do làm frozen trước là tạo mặt bằng ít tốn tối ưu hơn để khảo sát biểu diễn. Nó không thay thế phép so tinh chỉnh, vì backbone chưa được học lại theo nhãn đích.

## Bước 3: frozen và LoRA của ESM2-35M phải khớp runtime

**LoRA** thêm một cập nhật ma trận hạng thấp vào trọng số nền, giữ trọng số nền đóng băng. Viết $W'=W+(\alpha/r)BA$: r là rank, A và B là hai ma trận nhỏ được học. [TL-05]

Ví dụ **tự đặt**: W có 512×512 phần tử; với r=8, A có 8×512 và B có 512×8, tổng 8.192 tham số thay vì 262.144. Đây chỉ là ví dụ đếm một ma trận, không phải số tham số thực của toàn ESM2-35M hay toàn adapter.

Protocol chọn LoRA ở attention Q/V, rank 8, alpha 16; head 64, ReLU, dropout 0,2. AdamW dùng learning rate 0,0001, weight decay 0,01; batch 8, float32, clip gradient 1, tối đa 20 epoch và patience 4. **Learning rate** là cỡ bước cập nhật; **batch** là số mẫu mỗi bước; **patience** là số epoch chờ validation cải thiện trước dừng sớm. [KH-02; KH-03]

Hai nhánh frozen và LoRA cần cùng split, head initialization và chính sách dropout backbone. Dùng `eval` cho backbone để khớp dropout không đồng nghĩa tắt gradient của adapter: chế độ layer và cờ gradient là hai khái niệm khác nhau. Runner còn phải kiểm tham số LoRA thật sự thay đổi, tránh một “fine-tune” chỉ học head.

**Inner MSE** chọn epoch; sau đó refit outer-train đúng số epoch đã chọn. Không chọn epoch từ outer-test và không xem inner loss như MAE đánh giá cuối. Tuning model lớn hơn cần preflight riêng; không suy khả thi từ một cấu hình nhỏ.

![Các bước còn phải hoàn tất theo kế hoạch local. Mọi hộp vàng là hướng thực thi/kiểm chứng, không phải bảng tiến độ đã đạt.](assets/diagrams/local-training-plan.pdf){width=91%}

## Bước 4: đủ OOF rồi mới kết luận

**Checkpoint** lưu trạng thái để tiếp tục công việc: adapter/head, optimizer, tiến độ và identity liên quan. **Resume** chỉ hợp lệ khi manifest khớp. Một checkpoint thành công ở một fold là kết quả thực thi cục bộ; chưa đủ ensemble, CI hoặc xếp hạng scientific.

Đích tiếp theo là collect đủ fold/seed, kiểm row coverage, gộp OOF, tính metric cùng cohort và CI ghép cặp. Bảng khảo sát nhiều pLM vẫn là development; không chọn family từ outer OOF rồi gọi điểm chính bảng đó là đánh giá độc lập của lựa chọn.

## Bước 5: giữ T khóa và phân biệt export với promotion

Recipe **W5-D** đã được chỉ định cho held-source T; không dùng kết quả T để chọn pLM, ngưỡng hoặc epoch. T từng được khảo sát ở mức nguồn trong lịch sử, nên không gọi là external hoàn toàn chưa đụng tới. [KH-01; KH-02]

**Export** tạo gói suy luận; **promotion** đưa phiên bản vào phục vụ sau kiểm chứng. Runner có đường refit/export W5; family/CNN/LoRA còn thiếu tự động hóa final promotion. Có code chưa đồng nghĩa có artifact cuối đã nghiệm thu.

**Vận dụng:** vẽ lại hai nhánh frozen/LoRA và chỉ nơi chọn epoch, collect OOF, khóa T. Bài thực hành buổi 5 ở [chặng 17](#practice) có các điểm cần tự kiểm.
