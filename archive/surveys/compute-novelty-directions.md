# Hướng đề tài có tính mới ở phần tin học

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../DECISIONS.md).

Ngày khảo sát: **08/10/2026**. Câu hỏi của sinh viên: các ứng viên hiện tại (A — cơ chất SIRT theo isoform, B — vị trí phospho theo nhóm kinase) đều đặt tính mới ở **vấn đề sinh học**; cần tìm thêm hướng mà tính mới nằm ở **phần tin học**: cải tiến mô hình, cách xử lý mới cho bài toán cũ, chính xác hơn, rẻ hơn hoặc nhanh hơn.

Tài liệu này **không chốt hướng**. Mỗi nhận định về "chưa ai làm" chỉ dựa trên vài lượt tìm web ngày 08/10, nên đều mang nhãn **[chưa kiểm sâu]** cho tới khi đọc đủ bài liên quan.

## 0. Kết luận trước

1. **Một hướng "cải tiến tin học" chỉ đứng được khi có thước đo chung để so.** Tức là phải có benchmark công khai, có baseline chạy lại được, và cách chia tập kiểm soát đồng dạng. Thiếu điều này thì "tăng 2% accuracy" không chứng minh được gì, và GVHD đã nêu cổng dữ liệu (tập test độc lập) ngay từ buổi 1.
2. **Bẫy lớn nhất của loại đề tài này: cải tiến nhỏ trên benchmark đã bão hòa.** Nhiều benchmark tin sinh (ví dụ peptide kháng ung thư ACP740) đã có hàng chục bài, mỗi bài hơn bài trước 1–3%, thường do rò rỉ đồng dạng chứ không phải do phương pháp. Làm thêm một bài như vậy khó qua tiêu chí 1.
3. Từ các lượt tìm, có **ba kiểu đóng góp tin học đo được** và hợp với nền của GVHD (PLM + mCNN trên trình tự):
   - **Nhanh/rẻ hơn:** nén mô hình PLM + CNN thành mô hình nhỏ chạy CPU, đo đánh đổi độ chính xác và thời gian (C1).
   - **Biểu diễn mới hơn PLM thuần trình tự:** dùng token cấu trúc 3Di (ProstT5 hoặc SaProt), đúng câu GVHD hỏi ở tiêu chí 3 "có gì mới hơn PLM không" (C3). Nhưng nhóm GVHD đã thử ProstT5, xem bên dưới.
   - **Đầu ra đáng tin hơn:** dự đoán có bảo đảm thống kê (conformal prediction), cho biết khi nào mô hình không chắc (C4).
4. Ba kiểu này **có thể gắn lên A hoặc B** thay vì bỏ chúng: bài toán sinh học giữ nguyên, phần tin học là đóng góp chính. Đây là điểm nên cân nhắc trước khi mở hẳn một hướng mới.
5. Nếu muốn một hướng **độc lập, đúng chủ đề aging, có benchmark sẵn**: đồng hồ methyl hóa DNA trên **ComputAgeBench** (C6). Rủi ro: GVHD chưa làm methylation, dữ liệu 38,6 GB.

**Phát hiện cần biết:** bài RAG-msCNN của chính GVHD (2026) **đã dùng ProstT5 làm baseline** và kết luận nó không cải thiện đáng kể (mục C3). Vì vậy C3 không còn là lá bài mạnh như lúc đầu tưởng.

**Gợi ý của tôi (không phải quyết định):** ưu tiên xem **C1 (nén mô hình) kèm C4 (conformal) gắn lên B**, vì B là ứng viên duy nhất đã có benchmark cộng đồng, nên phần cải tiến đo được ngay. Lý do và điều kiện ở mục 4.

> **Bước tiếp theo (08/10):** sinh viên chọn giữ A/B và có GPU; bản phác cụ thể nằm ở [b-method-layer-draft.md](b-method-layer-draft.md).

## 1. Thước đo để xếp các hướng

Ngoài năm tiêu chí của GVHD ([biên bản lần 1, mục 4](../../project/meetings/2026-10-02-session-01/minutes.md)), một hướng tin học cần thêm ba điều kiện:

| Điều kiện | Vì sao |
|---|---|
| **Benchmark công khai, tập test độc lập** | Không có thì không so được với phương pháp cũ |
| **Baseline có mã, chạy lại được** | Phải tự chạy lại baseline trên cùng cách chia, không chép số từ bài báo |
| **Chạy được bằng tài nguyên sẵn có trong 8–9 tuần** | Máy không có GPU; Colab/Kaggle chưa dùng ([resources.md](../../resources/README.md)) |

## 2. Các hướng đã khảo sát

### C1. Nén mô hình PLM + CNN để chạy nhanh trên CPU (nhanh hơn, rẻ hơn)

- **Vào/ra:** giống bài toán gốc (ví dụ cửa sổ quanh S/T/Y → xác suất phospho, hoặc chuỗi → nhãn từng residue gắn ATP). Đóng góp nằm ở mô hình **học trò** nhỏ được chưng cất (knowledge distillation) từ mô hình **thầy** ESM-2/ProtT5 + mCNN.
- **Vì sao cần:** trích embedding PLM tốn tài nguyên. Bài KD_MultiSucc ghi rõ embedding ProtT5 là 1024 chiều cho mỗi amino acid và tốn kém khi sinh ra. Website (tiêu chí 5) chạy trên máy chủ không GPU thì mô hình nhỏ là lợi ích thật cho người dùng.
- **Đã có gì:** chưng cất đã dùng cho PTM (KD_MultiSucc cho succinyl hóa, một bài ubiquitin ở *Arabidopsis*), và DistilProtBert ở mức embedding. **Không tìm thấy** bài chưng cất PLM cho dự đoán theo residue có báo cáo độ trễ CPU **[chưa kiểm sâu]**.
- **Đo được gì:** đường MCC/AUPRC theo thời gian suy luận và bộ nhớ trên CPU; so với mô hình thầy và baseline không dùng PLM.
- **Ưu:** khớp nền GVHD (mCNN); kết quả hiển thị trực tiếp trên website; dễ đặt cổng dừng (học trò mất quá X điểm MCC thì dừng).
- **Nhược:** người chấm có thể xem là "kỹ thuật" hơn "khoa học" nếu không kèm phân tích vì sao học trò giữ được thông tin; cần GPU một lần để sinh nhãn mềm từ mô hình thầy (Colab đủ, chưa đo).
- **Tiêu chí GVHD:** 2 (cải tiến phương pháp) mạnh, 5 mạnh, 1 trung bình, 3 yếu, 4 làm thêm được.

### C2. Tinh chỉnh LoRA thay cho embedding đóng băng

- **Ý:** các công trình cùng nhánh GVHD thường dùng embedding PLM đóng băng rồi đưa vào CNN. Schmirler, Heinzinger, Rost (*Nat Commun* 2024) cho thấy tinh chỉnh **gần như luôn** cải thiện dự đoán, và LoRA đạt mức tương tự với chi phí thấp hơn, huấn luyện nhanh tới 4,5 lần.
- **Đã có gì:** ESMBind/QBind (bioRxiv 2023) áp LoRA cho vị trí gắn và PTM; PhosF3C áp LoRA cho phospho; ESM-LoRA-Gly (bioRxiv 2025) cho glycosyl hóa. Vì vậy **"dùng LoRA" tự nó đã không còn mới**.
- **Phần còn mở [chưa kiểm sâu]:** ghép LoRA với đầu mCNN nhiều cửa sổ và so có kiểm soát (cùng cách chia, cùng đầu) với cách đóng băng mà nhóm GVHD đang dùng.
- **Nhận xét:** hợp làm **một nhánh thí nghiệm** trong C1 hoặc C3 hơn là đề tài riêng. Cần GPU.

### C3. Biểu diễn có thông tin cấu trúc: token 3Di (ProstT5, SaProt)

- **Ý:** trả lời thẳng câu hỏi ở tiêu chí 3, khi GVHD lấy ví dụ PSSM → PLM rồi hỏi "có gì mới hơn không". Bước kế tiếp hợp lý là **PLM biết cấu trúc**:
  - **SaProt** (ICLR 2024) ghép token amino acid với token cấu trúc 3Di của Foldseek, huấn luyện trên khoảng 40 triệu chuỗi kèm cấu trúc.
  - **ProstT5** tinh chỉnh từ ProtT5 để dịch qua lại giữa chuỗi và 3Di. Điểm quan trọng: **3Di có thể dự đoán từ chuỗi**, nên không cần file cấu trúc. Chỉ cần cấu trúc khi muốn 3Di "thật" (AlphaFold DB).
- **⚠️ Nhóm GVHD đã thử ProstT5.** Bài RAG-msCNN (2026, GVHD là tác giả liên hệ; PDF trong [advisor/Prof Ho/](../../resources/papers/ho-quang-thai/), `1-s2.0-S1746809425019184-main.pdf`) dùng embedding ProstT5 làm một baseline cho vị trí gắn protein–DNA, và ghi ProstT5 "failed to significantly improve predictions" (F1 0,2353, MCC 0,2726 trên một tập test; ESM-2, ESM-C, ProstT5 đều quanh MCC dưới 0,39). Hệ quả: GVHD đã biết ProstT5 và đã thấy nó **không giúp nhiều** trên bài của thầy. Đề xuất "đổi sang ProstT5" sẽ dễ bị hỏi lại "nhóm thầy thử rồi". Ngược lại, con số RAG-ProtTrans (MCC khoảng 0,91) mà bài đó dùng để so có những vấn đề đã ghi ở [rag-mscnn-verification.md](bioinformatics-topic-survey/rag-mscnn-verification.md) (ngưỡng chọn trên tập test, tập test RNA đã cân bằng), nên kết luận "ProstT5 kém" trong bài cũng chưa phải phép so sạch.
- **Đã có gì ngoài nhóm GVHD:** GraphPBSP tự nhận là bài đầu tiên dùng embedding ProstT5 cho vị trí gắn protein–protein/peptide, nhưng không tách riêng phần đóng góp của ProstT5. Brabec và Hoksza (BIBM 2024) cho thấy thêm đặc trưng cấu trúc đơn giản giúp mô hình ESM-2 dự đoán vị trí gắn tốt hơn. **Không tìm thấy** phép so có kiểm soát giữa ProtT5/ESM-2 và ProstT5/SaProt, cùng một đầu CNN, cho vị trí phospho hoặc vị trí gắn ATP/FAD **[chưa kiểm sâu]**.
- **Đo được gì:** thí nghiệm cắt bỏ sạch (ablation): giữ nguyên đầu mCNN, chỉ đổi biểu diễn (ESM-2 → ProtT5 → ProstT5 chỉ AA → ProstT5 AA+3Di → SaProt). Thêm một câu hỏi phụ có giá trị: **3Di dự đoán từ chuỗi có kém 3Di từ AlphaFold không?** Nếu không kém, website chỉ cần nhận chuỗi.
- **Ưu:** đúng tiêu chí 3; dùng lại nguyên khung PLM + mCNN của T1 và của GVHD; XAI có thêm chiều mới (occlusion trên token cấu trúc so với token trình tự).
- **Nhược:** ProstT5 là mô hình 3B tham số. Trích embedding trên CPU có thể rất chậm, cần đo thử trên vài trăm chuỗi trước khi cam kết. Với vị trí PTM nằm ở vùng mất trật tự (disordered), 3Di có thể ít thông tin, nên kết quả âm là khả năng thật. Kết quả âm vẫn báo cáo được, nhưng phải nói trước với GVHD.
- **Phần còn có thể mới, sau khi biết nhóm GVHD đã thử ProstT5:** (a) SaProt chưa thấy trong bài của nhóm; (b) dùng **chuỗi token 3Di** làm kênh đầu vào riêng cho mCNN, thay vì chỉ lấy embedding ProstT5; (c) so 3Di dự đoán với 3Di từ AlphaFold. Cả ba vẫn **[chưa kiểm sâu]**.
- **Tiêu chí GVHD:** 3 trung bình (đã giảm từ "mạnh" vì nhóm GVHD đã thử ProstT5), 2 trung bình, 4 làm thêm được, 5 được, 1 thấp–trung bình.

### C4. Dự đoán có bảo đảm thống kê (conformal prediction)

- **Ý:** thay vì chỉ ra xác suất, mô hình trả về tập nhãn có bảo đảm, ví dụ "đúng ít nhất 90% số lần". Người dùng website biết khi nào mô hình không chắc. Đây là phiên bản có nền lý thuyết của ý "cảnh báo miền áp dụng" trong hướng RTK–ATP cũ.
- **Đã có gì:** conformal đã dùng cho cấu trúc protein (CalPro, ICML 2026) và tìm kiếm protein (Boger và cộng sự). **Không tìm thấy** bài áp conformal cho dự đoán vị trí PTM **[chưa kiểm sâu]**.
- **Đo được gì:** độ phủ thực tế so với mức đặt trước, kích thước tập dự đoán, và độ phủ theo nhóm (theo kinase, theo độ đồng dạng với tập huấn luyện).
- **Ưu:** rẻ, chạy trên CPU, đặt lên bất kỳ mô hình nào; hợp tiêu chí 5.
- **Nhược:** cần một tập hiệu chỉnh tách riêng, nên ăn bớt dữ liệu, bất lợi với A vốn đã ít dữ liệu. Một mình C4 có thể bị xem là mỏng, nên ghép với C1 hoặc C3.

### C5. Cải tiến mô hình trên chính B: dự đoán cho kinase ít hoặc chưa có dữ liệu

- **Ý:** hơn 95% vị trí phospho người đã biết chưa rõ kinase nào gắn. Bài toán zero-shot là dự đoán cho kinase chưa có vị trí đã biết, bằng cách học biểu diễn của chính kinase.
- **Đã có gì:** DeepKinZero (*Bioinformatics* 2020, mã công khai) là baseline sẵn. Tên Phosformer không tìm ra bằng tìm web, cần tra lại **[chưa kiểm]**.
- **Ưu:** khớp chủ đề cancer (kinase); bài toán cũ, cách xử lý mới (embedding kinase bằng PLM thay biểu diễn của bài 2020).
- **Nhược:** đánh giá zero-shot dễ rò rỉ (kinase cùng họ rất giống nhau), phải chia theo họ kinase; đã có preprint cạnh tranh ở B (ghi trong phân tích trước).

### C6. Hướng độc lập, chủ đề aging: đồng hồ methyl hóa DNA trên ComputAgeBench

- **Vào/ra:** vector methyl hóa CpG của một mẫu máu → tuổi sinh học. Đầu vào dạng ma trận, GVHD đã chấp nhận loại đầu vào này (ghi nhận 07/10).
- **Benchmark:** **ComputAgeBench** (Kriukov và cộng sự, KDD 2025): 66 bộ dữ liệu máu công khai, 19 tình trạng làm tăng tốc lão hóa, 13 đồng hồ đã công bố. Điểm hay: không chấm bằng MAE với tuổi thật, mà chấm khả năng **tách người bệnh khỏi người khỏe**. Đây đúng là chỗ trả lời câu "tuổi sinh học không có nhãn chuẩn". Dữ liệu trên Hugging Face, giấy phép CC BY-SA 4.0, **truy cập được từ môi trường cloud (thử 08/10, mã 200)**.
- **Đóng góp tin học có thể có:** mô hình mới (ví dụ thay ElasticNet bằng mô hình nhỏ có ràng buộc, chọn CpG có kiểm soát) và XAI chỉ ra CpG nào đẩy dự đoán.
- **Ưu:** benchmark chuẩn, mới, chưa đông; đúng chủ đề aging; chạy CPU được nếu lọc CpG.
- **Nhược lớn:** GVHD **không có công trình methyl hóa** trong danh mục ([advisor/README.md](../../project/advisor-research.md)), lệch xa khung PLM + mCNN; dữ liệu đầy đủ **38,6 GB** (khoảng 17,8 nghìn mẫu × 900 nghìn CpG), vượt dung lượng một phiên cloud, phải tải từng phần; khó giải thích lợi ích cho người dùng website.

### C7. Hướng độc lập, chủ đề cancer: dự đoán đáp ứng thuốc liên bộ dữ liệu

- **Benchmark:** IMPROVE (nhóm Argonne, *Brief Bioinform* 2026): 5 bộ sàng lọc thuốc công khai, 7 mô hình chuẩn hóa, mã và cách chia công khai. Kết luận chính: hiệu năng **giảm mạnh** khi gặp bộ dữ liệu chưa thấy, và không mô hình nào thắng mọi trường hợp. Đó là khoảng trống tin học rõ ràng (khả năng tổng quát hóa).
- **Nhược:** xa nền GVHD nhất; mô hình đa phương thức (thuốc + tế bào) nặng; lĩnh vực đông nhóm lớn.
- **Nhận xét:** để tham khảo, không khuyên chọn.

### Đã xem và loại: peptide kháng ung thư (ACP)

Có benchmark (ACP740, ACPmain, ACPalter) và rất nhiều bài dùng ESM-2/ProtT5 trong 2024–2025 (PLMACPred, ACP-CLB, ACP-CapsPred). Lý do loại: **quá đông**, và **trùng gần như hoàn toàn với luận văn T1** cùng GVHD (sàng lọc peptide bằng PLM + mCNN). Khó qua tiêu chí 1.

## 3. Bảng so sánh

| | C1 Nén | C3 Token cấu trúc | C4 Conformal | C5 Kinase zero-shot | C6 Đồng hồ methyl | C7 Đáp ứng thuốc |
|---|---|---|---|---|---|---|
| Kiểu cải tiến | Nhanh, rẻ | Biểu diễn mới | Tin cậy | Tổng quát hóa | Mô hình mới | Tổng quát hóa |
| Gắn được lên A/B | Có | Có | Có | Chỉ B | Không | Không |
| Benchmark sẵn | Theo bài gốc | Theo bài gốc | Theo bài gốc | DeepKinZero | ComputAgeBench | IMPROVE |
| Khớp GVHD | Cao | Cao, nhưng nhóm GVHD đã thử ProstT5 | Trung bình | Trung bình | Thấp | Thấp |
| Tiêu chí 1 / 2 / 3 / 4 / 5 | TB / Cao / Thấp / Được / Cao | Thấp–TB / TB / TB / Được / Được | TB / TB / TB / — / Cao | TB / Cao / TB / Được / Được | Cao / TB / TB / Được / TB | TB / TB / TB / Được / TB |
| Cần GPU | Một lần (nhãn mềm) | Có thể (ProstT5 3B) | Không | Có thể | Không | Có |
| Rủi ro chính | Bị xem là kỹ thuật | Kết quả âm ở vùng mất trật tự | Mỏng nếu đứng riêng | Rò rỉ theo họ kinase | Lệch GVHD, 38,6 GB | Xa GVHD, nặng |

"TB" = trung bình. Các ô đánh giá là nhận định của tôi từ tài liệu trên, chưa có thực nghiệm.

## 4. Gợi ý và lý do

**Gợi ý: B làm bài toán, C1 (nén mô hình) làm đóng góp chính, C4 (conformal) làm phần phụ; C3 chỉ là một nhánh thí nghiệm (thêm SaProt và kênh 3Di vào bậc thang biểu diễn).** Lý do:

- B là ứng viên duy nhất có benchmark cộng đồng (dbPTM không đồng dạng), nên điều kiện quan trọng nhất của một đề tài tin học (so được với cái cũ) đã có sẵn.
- C1 giữ nguyên khung PLM + mCNN mà GVHD quen, và cho một lợi ích người dùng thấy được trên website (chạy nhanh trên máy không GPU). Đây là chỗ nối tự nhiên giữa tiêu chí 2 và tiêu chí 5, hợp với khoa Kỹ thuật phần mềm.
- C4 rẻ, chạy CPU, và cho website một tính năng có nền lý thuyết: báo khi nào dự đoán không đáng tin.
- C3 bị hạ xuống nhánh phụ vì nhóm GVHD đã thử ProstT5 trong RAG-msCNN và không thấy lợi.
- Nhược điểm của B (GVHD chưa làm phospho, có preprint cạnh tranh) giảm bớt khi đóng góp chuyển sang phần phương pháp: bài toán phospho chỉ là nơi để đo.

**Khi nào gợi ý này sai:**

- Nếu học trò nhỏ mất quá nhiều độ chính xác so với mô hình thầy (ví dụ hơn 0,05 MCC; ngưỡng này là đề xuất, cần chốt trước khi chạy), C1 thành kết quả âm. Khi đó đóng góp chính chuyển sang C4 cộng phân tích lỗi.
- Nếu GVHD muốn tính mới ở bài toán (tiêu chí 1) hơn ở phương pháp, thì A vẫn mạnh hơn. C3/C4 vẫn gắn được lên A, nhưng thiếu tập test độc lập vẫn là điểm yếu của A.
- Nếu sinh viên muốn hẳn một hướng aging mới, C6 là lựa chọn duy nhất có benchmark chuẩn; phải hỏi GVHD có chấp nhận methyl hóa không.

**Việc nên làm trước tuần 6, theo thứ tự:**

1. Đo thời gian trích embedding ESM-2 (bản 150M và 650M) trên CPU cho khoảng 200 cửa sổ phospho, để có mốc "mô hình thầy chậm cỡ nào" cho C1.
2. Đọc kỹ: Schmirler 2024, KD_MultiSucc, và mục kết quả của RAG-msCNN chỗ so ProstT5, để kiểm lại các ô **[chưa kiểm sâu]** ở trên.
3. Thêm vào danh sách câu hỏi tuần 6: *"Thầy có chấp nhận đóng góp chính nằm ở phương pháp (biểu diễn mới, nén mô hình) trên một bài toán đã có benchmark không?"*

## 5. Nguồn

- Schmirler, Heinzinger, Rost (2024), *Fine-tuning protein language models boosts predictions across diverse tasks*, Nat Commun — [PMC11358375](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11358375/)
- ESMBind và QBind — [bioRxiv 2023.11.13.566930](https://www.biorxiv.org/content/10.1101/2023.11.13.566930.full.pdf) · ESM-LoRA-Gly — [bioRxiv 2025.08.12.669850](https://www.biorxiv.org/content/10.1101/2025.08.12.669850.full.pdf) · PhosF3C — [CityU](https://scholars.cityu.edu.hk/en/publications/phosf3c-a-feature-fusion-architecture-with-fine-tuned-protein-lan/)
- KD_MultiSucc — [PMC12202750](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12202750/) · Multi-teacher distillation cho embedding protein — [arXiv 2405.11735](https://arxiv.org/html/2405.11735v1)
- SaProt — [ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/1c42513b8895ab11fbbb5b7e8e6b6b02-Paper-Conference.pdf) · ProstT5 — [bioRxiv 2023.07.23.550085](https://www.biorxiv.org/content/10.1101/2023.07.23.550085.full.pdf), [model card](https://huggingface.co/Rostlab/ProstT5) · Brabec và Hoksza, BIBM 2024 — [trang công bố](https://www.d3s.mff.cuni.cz/publications/brabec_integrating_2024/)
- CalPro — [arXiv 2601.07201](https://arxiv.org/abs/2601.07201)
- DeepKinZero — [bioRxiv 670638](https://www.biorxiv.org/content/10.1101/670638.full.pdf)
- ComputAgeBench — [bioRxiv 2024.06.06.597715](https://www.biorxiv.org/content/10.1101/2024.06.06.597715.full.pdf), [dữ liệu](https://huggingface.co/datasets/computage/computage_bench)
- IMPROVE, benchmark đáp ứng thuốc — [PMC12794626](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12794626/)
- PLMACPred (ACP) — [PMC11266708](https://pmc.ncbi.nlm.nih.gov/articles/PMC11266708/)
- Bộ ATP-388/41, ATP-227/17 (bối cảnh nhánh GVHD) — [arXiv 2402.01829](https://arxiv.org/pdf/2402.01829)

## 6. Điều tài liệu này chưa làm

- Chưa đọc toàn văn bài nào; mọi nhận định dựa trên tóm tắt và kết quả tìm web.
- Chưa chạy thử bất kỳ mô hình nào, chưa đo thời gian CPU.
- Đã quét 6 PDF của GVHD trong repo tìm các từ ProstT5, SaProt, distill, conformal, LoRA: chỉ RAG-msCNN có ProstT5 (đã ghi ở C3); chữ "distilled" trong mCNN-ETC không phải nén mô hình; "fine-tuning" xuất hiện ở hai bài nhưng chưa đọc ngữ cảnh. Danh mục 14 bài có thể chưa đủ ([advisor/README.md](../../project/advisor-research.md)), nên vẫn cần đối chiếu thêm trước khi tuyên bố tính mới.
