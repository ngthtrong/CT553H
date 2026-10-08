# Bản phác: ứng viên B kèm cải tiến tin học (nén mô hình + conformal)

Ngày: **08/10/2026**. Tiếp nối [compute-novelty-directions.md](compute-novelty-directions.md). Sinh viên đã chọn: **có GPU (Colab/Kaggle)**, và **giữ A/B, thêm cải tiến tin học lên trên**. Đây là bản phác để mang đi bàn với GVHD tuần 6, **chưa phải đề tài đã chốt**.

Nhãn bằng chứng: `[tự đo]` là số Claude tự tải và đếm ngày 08/10; `[chưa kiểm]` là suy luận hoặc chỉ thấy qua tóm tắt.

## 0. Ba điều mới phát hiện, phải biết trước

1. **Benchmark dbPTM không có sẵn chia train/test.** Mỗi nhóm kinase chỉ có hai file FASTA cửa sổ 21 residue (±10): `*_pos.fasta` và `*_neg.fasta`, ngày file 14/08/2018. dbPTM mô tả nó là bộ dữ liệu để **đánh giá các công cụ đã huấn luyện ở nơi khác**. Với CDK: **1.503 cửa sổ dương, 29.823 cửa sổ âm**, 789 protein ở tập dương, không có cửa sổ nào trùng giữa dương và âm `[tự đo]`. Hai cột số trên trang download khớp đúng hai con số này; cột đầu (1.020) chưa rõ nghĩa.
2. **File thực nghiệm `Phosphorylation.gz` của dbPTM (33 MB) không có cột kinase** `[tự đo]`: chỉ có tên protein, accession, vị trí, loại PTM, PMID và cửa sổ. Muốn **huấn luyện** theo nhóm kinase thì phải lấy nhãn kinase từ nguồn khác.
3. **Nguồn nhãn kinase mở, tải được ngay:** API OmniPath `enz_sub` trả về **39.036 dòng** kinase–cơ chất–vị trí ở người, kèm cột nguồn (PhosphoSite, SIGNOR, phosphoELM, HPRD, dbPTM…) `[tự đo]`. UniProt REST cũng truy cập được (200), nên trích lại cửa sổ rộng hơn ±10 là khả thi.

**Hệ quả cho câu chuyện của B:** "B có tập test độc lập sẵn" chỉ đúng một nửa. Tập test thì có (benchmark dbPTM), nhưng tập train phải tự dựng từ OmniPath, rồi **lọc bỏ mọi protein đồng dạng với protein trong benchmark** (CD-HIT hoặc MMseqs2 ở mức protein). Không thể tách theo nguồn, vì OmniPath và dbPTM cùng gom từ PhosphoSite, phosphoELM… nên trùng nhau nhiều `[chưa kiểm]`. Đây vẫn là thế mạnh hơn A, nhưng phải nói đúng như vậy với GVHD.

## 1. Tên đề tài tạm

**Dự đoán vị trí phosphoryl hóa theo nhóm kinase bằng PLM–mCNN được chưng cất cho suy luận nhanh trên CPU, kèm tập dự đoán có bảo đảm độ phủ (conformal prediction).**

## 2. Bài toán

- **Vào:** một chuỗi protein (người dùng dán vào website).
- **Ra:** với mỗi vị trí S/T/Y và mỗi nhóm kinase (CDK, MAPK, PKA, PKC, CK2, AKT, GSK…), một điểm xác suất **và** một tập dự đoán có bảo đảm, ví dụ "{CDK, MAPK} ở mức tin cậy 90%" hoặc "không chắc".
- **Kiểu học:** đa nhãn (một vị trí có thể bị nhiều nhóm phosphoryl hóa), mất cân bằng nặng (CDK khoảng 1 dương : 20 âm `[tự đo]`).

## 3. Kiến trúc dự kiến

| Thành phần | Nội dung | Vì sao |
|---|---|---|
| **Mô hình thầy** | ESM-2 (bản 650M) tinh chỉnh bằng LoRA + đầu mCNN nhiều cửa sổ, một đầu ra cho mỗi nhóm kinase | Mạnh nhất có thể trong khung GVHD quen; LoRA dùng GPU Colab |
| **Mô hình học trò** | CNN nhỏ trên one-hot/BLOSUM hoặc ESM-2 bản nhỏ (8M/35M), học từ nhãn mềm của thầy | Chạy nhanh trên CPU cho website |
| **Lớp conformal** | Mondrian conformal theo từng nhóm kinase, hiệu chỉnh trên tập tách riêng | Bảo đảm độ phủ cho từng nhóm, kể cả nhóm ít dữ liệu |
| **XAI** | Occlusion trên thầy và học trò | Xem học trò có học đúng "chỗ nhìn" của thầy không |

## 4. Câu hỏi nghiên cứu

- **RQ1 (tiêu chí 2, 3):** Trên benchmark dbPTM, tinh chỉnh LoRA cải thiện bao nhiêu so với embedding đóng băng (cách nhóm GVHD đang dùng), cùng một đầu mCNN?
- **RQ2 (tiêu chí 2, 5):** Học trò chưng cất giữ được bao nhiêu phần trăm MCC/AUPRC của thầy, với tốc độ suy luận CPU nhanh gấp bao nhiêu lần? So với học trò cùng kích thước nhưng huấn luyện không có thầy, để tách đúng phần lợi của chưng cất.
- **RQ3 (tiêu chí 5, độ tin cậy):** Conformal có giữ được độ phủ đặt trước cho từng nhóm kinase không, kể cả trên protein ít đồng dạng với tập train? Tập dự đoán to cỡ nào?
- **Phụ (tiêu chí 4):** XAI có tìm lại được motif đã biết không? Đây là phép kiểm có đáp án: CDK ưa proline ngay sau vị trí phospho. Trong benchmark, **1.246/1.503 (83%) cửa sổ dương CDK có P ở +1, so với 919/29.823 (3%) cửa sổ âm** `[tự đo]`. Nếu bản đồ occlusion không làm nổi vị trí +1 cho CDK thì XAI đang sai. Đây là kiểm tra tính trung thực mà luận văn T1 chưa có.

## 5. Bậc thang baseline

1. Motif/PSSM đơn giản (ví dụ quy tắc "S/T-P" cho CDK/MAPK). Mốc tối thiểu phải vượt.
2. One-hot + CNN.
3. ESM-2 đóng băng + mCNN (kiểu T1 và nhóm GVHD).
4. ESM-2 + LoRA + mCNN (mô hình thầy).
5. Học trò không chưng cất và học trò chưng cất.
6. Công cụ công bố có mã hoặc web server chạy được trên benchmark (KinasePhos 3.0, GPS; xem bảng dưới) `[chưa kiểm khả năng chạy]`.

## 6. Đối thủ và mức đông đúc

| Công trình | Liên quan | Ghi chú |
|---|---|---|
| **Prot2Token mở rộng cho kinase** (NeurIPS 2025) | PLM, dự đoán vị trí theo kinase, nhóm kinase, zero-shot cho kinase ít nghiên cứu | **Đối thủ trực tiếp nhất về độ chính xác.** Vì vậy đề tài không nên cạnh tranh bằng "chính xác hơn", mà bằng "nhanh hơn ở cùng mức chính xác, và có bảo đảm". Chưa đọc toàn văn `[chưa kiểm]` |
| KinasePhos 3.0 | 771 mô hình theo cá thể, họ, nhóm kinase | Cùng nhóm tác giả với dbPTM `[chưa kiểm]`; baseline tự nhiên |
| LMPhosSite | ProtT5 + gộp điểm, phospho tổng quát | Không theo kinase |
| KD_MultiSucc, KD_ArapUbi | Chưng cất cho succinyl hóa, ubiquitin | Tiền lệ chưng cất trong PTM; **không tìm thấy bài chưng cất cho phospho theo kinase** `[chưa kiểm sâu]` |
| (Conformal) | | **Không tìm thấy bài conformal cho vị trí phospho hay cơ chất kinase** `[chưa kiểm sâu]` |

## 7. Kế hoạch 8–9 tuần

| Tuần | Việc | Cổng dừng |
|---|---|---|
| 1 | Tải benchmark các nhóm, OmniPath, chuỗi UniProt; dựng train đã lọc đồng dạng với benchmark | Nếu sau lọc, nhóm nào dưới khoảng 100 vị trí dương ở train thì bỏ nhóm đó (ngưỡng đề xuất) |
| 2 | Baseline 1–3; đo thời gian CPU của ESM-2 | |
| 3 | Thầy LoRA (RQ1) | Nếu LoRA không hơn đóng băng, RQ1 thành kết quả âm, vẫn dùng mô hình tốt hơn làm thầy |
| 4–5 | Chưng cất, quét kích thước học trò (RQ2) | **Nếu học trò tốt nhất kém thầy hơn 0,05 MCC trung bình** (ngưỡng đề xuất, chốt trước khi chạy), đóng góp chính chuyển sang RQ3 |
| 5–6 | Conformal (RQ3), XAI | |
| 6–8 | Website: dán chuỗi → bảng điểm theo nhóm + tập conformal + bản đồ occlusion; chạy học trò trên CPU | |
| 9 | Viết, dự phòng | |

## 8. Áp sang A nếu GVHD chọn A

Khung giống hệt: thầy/học trò, conformal, XAI. Khác biệt: 7 nhãn SIRT1–7 thay cho nhóm kinase. Điểm yếu của A vẫn còn (không có tập test độc lập nguồn), và conformal cần tách thêm tập hiệu chỉnh từ 6.801 vị trí vốn đã ít.

## 9. Câu hỏi cho GVHD tuần 6

1. Thầy có chấp nhận đóng góp chính là **nén mô hình + bảo đảm thống kê**, không phải "chính xác hơn SOTA" không?
2. Tập test là benchmark dbPTM, tập train dựng từ OmniPath và lọc đồng dạng ở mức protein. Thầy có coi cách này là đủ độc lập không?
3. Với đầu mCNN nhiều cửa sổ, có cần cửa sổ rộng hơn ±10 của dbPTM không (trích lại từ UniProt được)?

## 10. Chưa làm

- Mới tải benchmark nhóm CDK; các nhóm khác chỉ đọc số trên trang download.
- Chưa tải toàn bộ OmniPath về đếm theo nhóm kinase, chưa đo mức trùng giữa OmniPath và benchmark.
- Chưa đọc toàn văn Prot2Token, KinasePhos 3.0, KD_MultiSucc.
- Chưa chạy mô hình nào, chưa đo thời gian CPU hay GPU.

## Nguồn

- dbPTM, trang download và benchmark theo nhóm kinase — https://biomics.lab.nycu.edu.tw/dbPTM/download.php
- OmniPath `enz_sub` — https://omnipathdb.org/enz_sub
- Prot2Token cho vị trí phospho theo kinase, NeurIPS 2025 — https://neurips.cc/virtual/2025/126023
- KinasePhos 3.0 — https://ngdc.cncb.ac.cn/biocode/tools/BT007291
- LMPhosSite — https://profiles.ncat.edu/en/publications/lmphossite-a-deep-learning-based-approach-for-general-protein-pho-2/
- KD_MultiSucc — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12202750/
- Schmirler và cộng sự 2024 (LoRA cho PLM) — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11358375/
