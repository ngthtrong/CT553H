# Plan-report đợt 1, phần Chương 3A/3B — 18/11/2026

Tiếp theo [report-validation-2026-11-18.md](report-validation-2026-11-18.md) (Chương 2). Phạm vi: mục
**4.1–4.5** và **5.1–5.6** của [plan-report.md](../plan-report.md), theo D-R1 = phương án A. Theo yêu cầu
của Trọng, **bỏ qua hình 5.2** (cổng miền đã có đủ ở dạng chữ trong mục *The Two-Tier Domain Gate*).
Không đổi số liệu, kết quả hay giới hạn bằng chứng; không chạy huấn luyện/suy luận; không commit/push.

## 1. Cấu trúc Chương 3

| Trước | Sau |
| --- | --- |
| 3.1 System Overview … 3.3 Data Design, 3.4 Research Progress, 3.5 Method and Model Design, 3.6 Implemented Features, 3.7 Local Execution View | **Part A: Research Method Design** (mục không đánh số, có trong mục lục): 3.1 Research Progress and Data Evolution, 3.2 Method and Model Design. **Part B: Software Design and Implementation**: 3.3 System Overview … 3.7 Local Execution View |

Trong 3.2:
- đoạn mở đầu mới và 2 hình (quy trình nghiên cứu, thiết kế thí nghiệm);
- mục mới *The Adapted Model LoRA-D* (hình kiến trúc) và *Final Refit and Locked Transfer Protocol*:
  hai đoạn "What was fixed before the outcome was seen" và "Refit design" được **chuyển nguyên văn** từ
  `transfer-refit.tex` (Ch.4), ở Ch.4 thay bằng đoạn *Protocol* ngắn trỏ về 3.2 và giữ giới hạn L1;
- mục *From Research Model to Served Model* (đoạn hai model phục vụ, trước ở đầu §Method);
- đoạn *Domain integration* bỏ vì trùng mục *The Two-Tier Domain Gate* ở Part B.

Chuyển sang Phụ lục A (mục A.4.1 *Campaign Recovery and Execution Environment*): mục *Research Campaign
and Recovery Design* (cùng hình lineage, giữ nhãn `sec:campaign-methods`) và đoạn môi trường thực thi.
Ở 3.2 thay bằng một câu trỏ sang phụ lục và giữ ý "không phải phép so có kiểm soát của riêng pretraining".

Sửa câu đã cũ trong `campaign-methods.tex`: "No LoRA model is selected or evaluated using T in the
completed campaign" → nói rõ là trong campaign development, còn refit khoá sau đó chấm LoRA-D trên T
một lần. Trang trạng thái nghiên cứu và mục *Structure and Status* của Mở đầu mô tả Part A/B.

## 2. Hình mới

| Mục | Tệp | Nguồn / đối chiếu |
| --- | --- | --- |
| 4.2 | `research-pipeline.tex` | `EXECUTION-PROTOCOL.md`, `PROTOCOL.md` refit, `model-card.json`, biên bản D-4 (Koren = khảo sát); số T từ macro |
| 4.3 | `lora-d-architecture.tex` | `degron_v3/finetune.py` (encoder dùng chung, Δ, 1020 → 64 → 1, AdamW 1e-4, wd 0.01, batch 8, clip 1), `model-card.json` (3 seed, 2 epoch, r = 8, α = 16, base revision qua macro), calibrator ba lớp |
| 4.4 | `experiment-design.tex` | RQ1–RQ5 của Mở đầu; khoảng tin cậy 98,75 % (4 contrast LoRA) và 97,5 % (2 contrast chuyển nguồn, `PROTOCOL.md`); mục Ch.4 dẫn bằng `\ref` |
| 5.1 | `app-predict-flow.tex` | `api/requests.py`, `api/service.py` (422 OUT_OF_DOMAIN trừ khi override), `prediction.py` |
| 5.4 | `app-tiling.tex` | quy tắc bước 23, chỉ cửa sổ đủ 28; ví dụ PTEN 403 aa → 17 cửa sổ, 397–403 không phủ (khớp màn hình job) |

## 3. Part B

- **5.3:** mục xếp hạng thêm câu nối với kết quả replay (macro `\nPriority…`), ghi rõ là bằng chứng development.
- **5.5:** ba quy tắc import đã có sẵn trong mục, giữ nguyên.
- **5.6:** comment `FROZEN until plan-system G-SYS` ở đầu Part B và trước §System Architecture, §Data Design,
  §Local Execution View. Không vẽ lại sơ đồ tổng thể nào.

## 4. Kiểm `[ĐO 18/11/2026]`

| Kiểm | Kết quả |
| --- | --- |
| `preview_figure.py` cho 5 hình | không overfull; đã xem từng ảnh, sửa đến khi hết chồng chữ |
| `make -C report all` | PASS |
| `make -C report check` | PASS — 164 trang một mặt, 164 hai mặt, smoke 9 |
| `check_float_references.py` | PASS — **41 hình, 64 bảng**, khớp cả hai bản |
| Mục lục | có dòng *Part A* / *Part B*; mục 3.1–3.7 đánh số liên tục |
| Khoảng trống > 1/3 (50 dpi, hai bản) | 12/164 trang, giống hệt; đều là trang kết thúc có chức năng: 5–6, 10, 17, 19, 22, 30, 54 (cuối Ch.2), 136, 140, 143, 164 |
| Ảnh render | 14 trang đầu Ch.3, trang hai hình tính năng, trang A.4.1 |

| PDF | SHA-256 |
| --- | --- |
| `report/build/content/content.pdf` | `148d21443e54ded8799165b1e38323b100aa1e35d1ecdb5fc48460d1f04be3e6` |
| `report/build/content-twoside/content.pdf` | `880774ba72df0d4be618c2e3c48253bc8d4b6d6260bb5c42d6770603b3f6c7be` |

## 5. Còn mở

- **4.5** chỉ làm một phần: đã chuyển chi tiết vận hành sang phụ lục, chưa viết lại từng thí nghiệm theo khuôn
  "mục đích → luồng → kết quả → giới hạn".
- **5.2** bỏ qua theo yêu cầu.
- Đợt 2 (7.x, 8.1) và đợt 3 (sau G-SYS) chưa bắt đầu.
