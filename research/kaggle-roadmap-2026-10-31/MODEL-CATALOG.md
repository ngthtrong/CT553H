# Danh sách model và chính sách khảo sát

**Cập nhật 01/11/2026:** registry đã pin revision20 checkpoint; download và hash đang được theo dõi trong [weights-status.json](weights-status.json). ESM2-8M đã được dùng train smoke frozen/LoRA trên nhãn thật. Chưa chạy benchmark official. Hidden size/parameter count/tài nguyên phải kiểm bằng stage02 trên runtime đích; revision lock không thay kiểm adapter.

## 1. Các họ và scale

| Họ | Checkpoint dự kiến | Vai trò |
|---|---|---|
| ESM-2 | 8M, 35M, 150M, 650M, **3B**, **15B** | 35M/650M neo R6; các cỡ còn lại kiểm scale. 15B cần sharding/offload/GPU đủ bộ nhớ sau preflight |
| ESM-1b | 650M | Đối chứng họ trước ESM-2 |
| ESM-1v | Năm checkpoint 650M, `_1…_5` | `_1` đơn và ensemble năm thành viên là hai recipe khác; không xem năm checkpoint là năm dataset |
| ESM-C | `biohub/ESMC-300M`, `ESMC-600M`, **`ESMC-6B`** | Khảo sát họ mới; dùng adapter/runtime riêng đã pin |
| ProtT5 | `Rostlab/prot_t5_xl_half_uniref50-enc` | Encoder-only half-precision; không nhầm số tham số toàn encoder-decoder với phần thực được dùng |
| Ankh | `ElnaggarLab/ankh-base`, `ankh-large` | Trích encoder representation; ghi cả checkpoint và encoder parameter count thực |
| SaProt | `westlake-repl/SaProt_35M_AF2`, `SaProt_650M_AF2` | Nhánh cấu trúc sau audit, cần true/masked 3Di cùng cohort |

Model IDs chi tiết trong JSON, dimension không hard-code cho họ mới trước tokenizer/forward probe. Không tự thêm Ankh3/ESM3 chỉ vì có model mới hơn; thay candidate list là phiên bản protocol mới.

## 2. Nguồn kiểm chứng

- [Meta ESM official](https://github.com/facebookresearch/esm): danh sách ESM-1b, năm ESM-1v, ESM-2 từ 8M đến 15B. IDs HF được kiểm thêm khi 02 resolve snapshot; không đồng nhất đường `esm.pretrained` với mọi API Transformers.
- [Biohub ESM official](https://github.com/Biohub/esm) và [ESMC-6B model card](https://huggingface.co/biohub/ESMC-6B): hiện có weights 6B công khai và hướng dùng local; tài liệu cũ gọi 6B chỉ API không còn được dùng làm kết luận hiện hành. [300M](https://huggingface.co/biohub/ESMC-300M), [600M](https://huggingface.co/biohub/ESMC-600M).
- [ProtT5 encoder model card](https://huggingface.co/Rostlab/prot_t5_xl_half_uniref50-enc): uppercase, encoder-only, T5 tokenizer; kiểm residue/special-token mask thay vì offset BOS/EOS kiểu ESM.
- [Ankh official](https://github.com/agemagician/Ankh), [base card](https://huggingface.co/ElnaggarLab/ankh-base), [large card](https://huggingface.co/ElnaggarLab/ankh-large): base/large có checkpoints riêng; card hiện ghi CC BY-NC-SA 4.0. Đọc tệp điều khoản của snapshot trước phân phối weights; không suy model quyền MIT từ package code.
- [SaProt official](https://github.com/westlake-repl/SaProt), [650M card](https://huggingface.co/westlake-repl/SaProt_650M_AF2): representation kết hợp amino acid với structural alphabet, có mask vùng độ tin cậy thấp. Model card không xác nhận cấu trúc protein nguyên vẹn phù hợp hoàn toàn assay peptide tách rời.

## 3. Ba mức thực nghiệm để đủ rộng nhưng có thể chạy

### Mức S — screen mọi family/scale khả thi

Frozen WT và Δ pooled + đầu tuyến tính chung. WT-only là đối chứng rẻ, **không thay** Δ pooled trong main matched-family comparison. Trích theo model/shard, cache tách. Model quá lớn có thể làm WT/MLM probe trước nhưng phải ghi rõ phần Δ chưa hoàn tất.

Chọn scale chính cho từng family bằng inner validation. Các checkpoint lớn 3B/6B/15B đều nằm trong kế hoạch tài nguyên; lỗi OOM/deferred phải có report, không diễn giải thành chất lượng sinh học kém.

### Mức H — head trên shortlist

ESM35 anchor + tối đa một family khác được chọn bằng nested rule. So pointwise/CNN/mCNN trên cùng thông tin. Không biến 20 checkpoint thành 20×3 heads×5 data arms×3 seeds×5 folds ngay từ đầu.

### Mức T — transfer sau khóa

Chỉ extract feature T của các recipe đã khóa, giữ context/projection/pooling/precision giống development. Không cần trích mọi model cho toàn bộ scan_T để bỏ phần lớn sau đó.

## 4. Dtype, tài nguyên và environments

- Frozen extraction không lưu gradient/optimizer của pLM. Stage04/05 train head mới; **stage11 bổ sung LoRA Q/V+head** và frozen comparator, optional full tuning8M/35M. Xem EXECUTION-PROTOCOL.md; không mở full tuning mọi model lớn theo mặc định.
- FP16/BF16/FP32 ghi trong config và output. Chọn theo phần cứng/runtime, chạy finite/repeatability probes; quantization là nhánh riêng, không dùng số của full-precision checkpoint để gọi đã tái lập quantized run.
- ESM2-15B cần ~30 GB decimal chỉ weights16-bit; ESMC6B ~12 GB decimal; còn activation, tokenizer buffers, framework, shard/offload overhead. Đây là phép tính lower-bound, chưa đo peak GPU RAM.
- Không giả hai T4 tạo một bộ nhớ chung tự động. Model dispatch/sharding/offload phải kiểm thật; nếu không đủ thời gian/RAM/disk thì báo `resource_blocked` và không chạy full pass.
- Mỗi family profile có lockfile/env report và adapter parity tests. Không cài các package cùng namespace `esm` đè nhau hoặc nâng Transformers giữa chừng mà reuse cache cũ.
- Không tải/pickle-execute mã từ raw data; weight loading và model code ở snapshot riêng đã review. Nếu cần official custom code, ghim source SHA và review trước thực thi; không blanket trust mọi repo.

## 5. Điều phải kiểm ở adapter

Chuỗi 28 AA phải cho đúng 28 residue representations sau bỏ special/pad tokens; test vị trí 1/2/14/27/28, mutation identity, WT→WT Δ=0, cùng thứ tự row IDs và chiều được ghi theo forward thực. ProtT5/Ankh spacing/tokenization khác ESM; SaProt dùng combined token khác sequence-only. Không lấy logits thay hidden state hoặc so final layer khác định nghĩa mà không ghi.

Layer choice mặc định final normalized representation theo adapter đã xác nhận. Nếu quét layer, đó là selection axis mới phải nằm trong inner tuning/budget, không thêm sau khi xem test.
