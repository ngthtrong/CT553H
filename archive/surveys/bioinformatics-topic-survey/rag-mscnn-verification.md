# Kiểm chứng mục 3.1 của báo cáo khảo sát tin sinh (RAG-msCNN)

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../DECISIONS.md).

> Kiểm ngày 01/10/2026. Claude tải trực tiếp mã nguồn thô và danh sách commit từ GitHub (repo [mhb1717/RAG_DNA_RNA](https://github.com/mhb1717/RAG_DNA_RNA)), rồi đối chiếu với bản PDF bài báo trong [advisor/Prof Ho/](../../../resources/papers/ho-quang-thai/) (`1-s2.0-S1746809425019184-main.pdf`). File này chỉ mô tả hành vi kỹ thuật của code và các con số, không kết luận về động cơ của tác giả. Người làm đề tài vẫn nên **tự mở lại các link dưới đây** trước khi dùng bất kỳ điểm nào khi trao đổi với thầy.

Báo cáo gốc: [bioinformatics-topic-survey.md](bioinformatics-topic-survey.md), mục 3.1.

## Kết quả theo từng dòng của bảng 3.1

| Dòng | Kết quả | Chi tiết đã thấy |
|---|---|---|
| 1. Script cũ chỉ làm giàu residue có nhãn dương | **Khớp** | Commit `05693c4` (01/07/2025 UTC). File `get_RagEmb_Batch_N.py` bắt buộc tham số `-labels`, dòng 72: `if label[1] == 1:  # Apply RAG only on positive samples`. Tại các commit `05693c4`, `f900b13` và `53a54f8` (02/07/2025), repo chỉ có một script RAG duy nhất, là script này. README lúc đó (`87e092e`) ghi các script RAG dùng "for training/testing" |
| 2. Bản viết lại không dùng nhãn | **Khớp** | `7a47d6a` (02/03/2026): `-labels` thành tuỳ chọn, "for statistics only". Script in ra "Applying RAG to ALL samples uniformly (no label-dependent processing)" và "RAG applied uniformly to all samples - no data leakage". File `get_RagEmbedding.py` hiện tại trộn 0,7/0,3 cho mọi truy vấn. Đợt viết lại kéo dài từ 28/02 tới 02/03/2026 |
| 3. Notebook hiện tại: MCC 0,2995 / 0,3979 / 0,4105 | **Khớp** | `MSCNN_DNA.ipynb` trên `main`, output đã lưu: TE181 MCC 0,2995 (AUC 0,8864), TE129 MCC 0,3979 (AUC 0,9131), TE46 MCC 0,4105 (AUC 0,8833) |
| 4. Baseline ProtTrans không RAG: 0,3033 / 0,3884 | **Khớp** | Bảng 4 của bài báo: TE181 ProtTrans MCC 0,3033 (AUC 0,894); TE129 ProtTrans MCC 0,3884 (AUC 0,917) |
| 5. TE117 (RNA) MCC 0,9431 ứng với tệp 4.424 hàng | **Khớp** | Notebook ở `b78474f`: test X = (4424, …), TP 1954, FP 68, TN 2345, FN 57, MCC 0,9431, AUC 0,9963. Bài báo ghi TE117 có 37.345 residue, trong đó 2.031 dương |
| 6. 2.413 = int(2.011 × 1,2), giống quy tắc trong `get_dataset_RAG_DB.py` | **Khớp** (phép tính và code) | 1954 + 57 = 2011 dương, 68 + 2345 = 2413 âm. Script `get_dataset_RAG_DB.py` dòng 103 dùng `num_negatives = int(len(positive_samples) * 1.2)` và chọn những âm có độ tương đồng cosine thấp nhất. Việc tệp TE117 được tạo bằng chính script này vẫn là suy luận |
| 7. Ngưỡng chọn bằng G-mean trên chính tập test | **Khớp** | Trong `model_test`, `roc_curve` chạy trên (X, y) đang đánh giá, sau đó lấy `argmax(gmeans)`. Notebook không có tập validation |
| 8. Bài báo không nhất quán nội bộ | **Khớp một phần** (đã thấy ở TE181) | Bảng 4 ghi TE181 RAG-ProtTrans F1 0,9123, MCC 0,8123, AUC 0,998. Phần kết quả và kết luận ghi MCC 0,9114, AUC 0,9998. AUC của TE129 cũng xuất hiện cả hai giá trị 0,9909 và 0,9999. Chưa kiểm phần TE46 |

## Điểm mới, báo cáo gốc chưa nêu

- Trong notebook **hiện tại** (bản không dùng nhãn), RNA TE117 vẫn chạy trên tệp 4.424 hàng và đạt MCC 0,8727. Nghĩa là bản viết lại chỉ bỏ việc dùng nhãn trong bước RAG. Tập test RNA vẫn là tập con đã cân bằng.
- Bài báo mô tả bước truy hồi là "retrieving the top five similar **binding** residue embeddings from our database". Trong khi đó, `get_dataset_RAG_DB.py` dựng CSDL gồm cả dương lẫn âm (tỉ lệ 1 : 1,2). Mô tả trong bài và code chưa khớp nhau.

## Chưa kiểm

- Chưa biết tệp `.npy` cụ thể nào sinh ra từng con số trong bài, vì các tệp sinh ra không có trong repo.
- Chưa giải nén `dna_dataset.rar` / `TE180.zip` nên chưa biết CSDL truy hồi có trùng protein với tập test không.
- Chưa chạy lại notebook. Mọi con số ở trên lấy từ output đã lưu sẵn trong notebook.
