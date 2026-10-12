# Bằng chứng cho đánh giá dark kinome trên DARKIN

Ngày kiểm: **10/10/2026**. Báo cáo: [dark-kinome-darkin-evaluation.md](../darkin-evaluation.md).

## 1. Artifact nội bộ và tái tạo

- [audit_data.py](audit_data.py): dùng thư viện chuẩn Python, đọc CSV và ma trận similarity đi kèm; không sửa checkout, không training.
- [audit-results.json](audit-results.json): count, per-kinase support, overlap, ngoại lệ residue trung tâm và SHA-256 dữ liệu/mã đã audit.
- Checkout phiên này: `/tmp/ct553h-darkin-review`, tài nguyên tạm có thể mất sau phiên. Không dùng đường dẫn tạm làm artifact lâu dài.
- Commit: `498de014951f962f77ca1b96340fead3cc24c450` của `https://github.com/tastanlab/darkin`.

```bash
git clone https://github.com/tastanlab/darkin.git /tmp/ct553h-darkin-review
git -C /tmp/ct553h-darkin-review checkout 498de014951f962f77ca1b96340fead3cc24c450
python3 topics/dark-kinome-zero-shot/research/darkin-audit/audit_data.py \
  --checkout /tmp/ct553h-darkin-review \
  --output topics/dark-kinome-zero-shot/research/darkin-audit/audit-results.json
```

Chạy từ root CT553H. Lệnh checkout chỉ dùng với clone riêng như trên. Không pin theo nhánh mặc định vì có thể drift. Script ghi commit thực tế; người tái lập cần đối chiếu commit/SHA đã công bố.

## 2. Quy tắc đếm

- Phosphosite key = `(SUB_ACC_ID, SUB_MOD_RSD)`; không đồng nhất key với chuỗi window.
- Kinase labels lấy từ `KINASE_ACC_IDS`, tách dấu phẩy, strip whitespace.
- Count pair là tổng số nhãn trong các dòng, không phải toàn bộ tích Descartes site × kinase.
- Overlap peptide được chuẩn hóa chữ hoa, giữ `_` padding; không coi annotation chữ thường là một trình tự khác.
- Similarity là trị số **ma trận gốc**, chưa tính alignment độc lập. Lưu số cặp kiểm/expected để phát hiện thiếu accession trong ma trận.
- Ngoại lệ trung tâm ngoài S/T/Y chỉ gắn cờ, không loại dòng; chưa kết luận metadata sai.
- Audit năm thư mục ZSL trực tiếp; không dùng `train_test_split/` lồng bên trong, không audit đầy đủ GZSL.

## 3. Bằng chứng metric trong mã nguồn pin

- [baseline_scripts/aupr_zsl.py](https://github.com/tastanlab/darkin/blob/498de014951f962f77ca1b96340fead3cc24c450/baseline_scripts/aupr_zsl.py): `ground_truth` dựng nhãn theo kinase; loop `average_precision_score` từng kinase rồi `np.mean`.
- [metrics.py](https://github.com/tastanlab/darkin/blob/498de014951f962f77ca1b96340fead3cc24c450/bilinear_zero_shot_model/scripts/evaluation/metrics.py): có macro AP theo kinase và macro row AP. Không đổi tên hai metric thành một mAP chung.

Đã đọc implementation; chưa chạy scoring trên dự đoán thật. Cần kiểm ordering site/kinase khi tái lập: thứ tự JSON/danh sách có thể quyết định alignment, không chỉ khớp shape. Chưa kết luận mã có lỗi hoặc đây chính là phiên bản sinh ra các số bài báo.

## 4. Hồ sơ nguồn trực tiếp

| Nguồn | Truy cập và phần dùng | Giới hạn |
|---|---|---|
| [DARKIN 2025](https://academic.oup.com/bioinformatics/article/41/11/btaf480/8306017) | HTML Methods/Results; split, metric, fine-tuning, mốc AP | Chưa tái lập training; code snapshot hiện tại có thể khác bản paper |
| [Repo DARKIN](https://github.com/tastanlab/darkin) | Clone và audit trực tiếp tại commit pin | Chưa mapping FASTA hoặc alignment độc lập |
| [Pekey 2025, metadata](https://research.sabanciuniv.edu/id/eprint/53625/) · [PDF](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf) | PDF 93 trang; các phần Chương 3–4 liên quan attention, augmentation, LoRA, protocol | Đọc chọn phần liên quan, chưa audit code/training đầy đủ |
| [benchmarKIN 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12098709/) | Results/Methods phần thêm predicted relationships | Chưa tải/audit file hạ nguồn; không kết luận phủ dark kinase đủ |
| [Tài liệu benchmarKIN](https://benchmarkin.readthedocs.io/en/latest/notebooks/perturbBench.html) | Trang workflow perturbation benchmark truy cập được | Chưa chạy workflow hoặc thay thư viện |
| [COMPASS-PTM 2026](https://www.nature.com/articles/s41467-026-73148-3) · [code](https://github.com/ZhangJJ26/COMPASS-PTM) | Results DARKIN và code availability | Chưa đọc Supplementary S.3.7/clone code; cần khóa chiều AP và split |
| [Johnson 2023](https://www.nature.com/articles/s41586-022-05575-3) | Atlas và mô tả assay | Chưa tải PSSM/map overlap train-test |
| [Yaron-Barir 2024](https://www.nature.com/articles/s41586-024-07407-y) | Atlas, 78+15 kinase có hoạt tính Tyr | Không coi 93 là 93 conventional Tyr kinase |
| [KinoPlex 2026](https://www.nature.com/articles/s41587-026-03239-5) | Nội dung bài qua kết quả truy cập web, abstract/data availability | Chưa đọc toàn bộ supplementary, code hoặc audit validation |
| [Phosformer-ST](https://pmc.ncbi.nlm.nih.gov/articles/PMC10868336/) | Đoạn Results trong kết quả tìm kiếm; mở PMC bị challenge | Không gọi đã đọc toàn văn |
| [SAGEPhos, OpenReview](https://openreview.net/forum?id=hLwcNSFhC2) | Thấy bản nguồn nhưng trang/PDF trả challenge | Chưa đọc đủ; không coi access failure là không tồn tại |
| [Conformal beyond exchangeability](https://arxiv.org/abs/2202.13415) | Abstract về điều kiện exchangeability | Chưa thiết lập theorem riêng cho DARKIN |
| [Conformal for zero-shot models](https://arxiv.org/abs/2505.24693) | Abstract và setting CLIP | Không chuyển bảo đảm nguyên trạng sang unseen kinase classes |
| [XAI sanity checks](https://papers.nips.cc/paper/2018/hash/294a8ed24b1ad22ec2e7efea049b8737-Abstract.html) | Nguồn phương pháp để thiết kế kiểm tra | Chưa chạy XAI |

## 5. Giới hạn và đầu việc chưa làm

Chưa training, chưa có baseline tự tái lập, chưa kiểm chứng biological novelty. Chưa audit phân phối điều kiện assay, âm sinh học, nhãn thiếu, quyền tái phân phối và benchmark hạ nguồn. Conformal chưa có thiết kế đủ để hứa coverage. Source snapshot và số công bố là căn cứ khảo sát; kết quả model phải có config/split/seed/metric riêng khi bắt đầu thực nghiệm.
