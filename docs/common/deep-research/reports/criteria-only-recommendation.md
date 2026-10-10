# Nếu chỉ xét năm tiêu chí: đề tài nào?

Ngày: **10/10/2026**. Câu hỏi của sinh viên: *bỏ qua ràng buộc thời gian, lĩnh vực, độ liên quan tới đề tài của GVHD, và CPU/GPU; chỉ xét năm tiêu chí đánh giá — đề xuất đề tài nào?* Được tìm thêm, không bắt buộc dùng các ứng viên có trong repo.

Nhãn bằng chứng: `[tự đo]` = tài liệu này tự tải file và đếm trong phiên 10/10/2026; `[chưa kiểm]` = chỉ thấy qua tóm tắt tìm kiếm hoặc suy luận, chưa đọc toàn văn.

Năm tiêu chí lấy từ [biên bản buổi gặp lần 1, mục 4](../../../meeting/session-01-minutes.md): (1) tính mới của đề tài/hướng, (2) đề xuất hoặc cải tiến phương pháp, (3) sử dụng phương pháp mới, (4) XAI, (5) ứng dụng/website — tiêu chí 5 là thành phần không thể thiếu, và GVHD nói càng đạt nhiều càng tốt.

---

## 1. Đề xuất: một đề tài

**Gán kinase cho vị trí phosphorylation chưa có chú giải, bao gồm các kinase ít được nghiên cứu (dark kinome): mô hình điều kiện theo kinase, tập dự đoán có bảo đảm phủ, XAI đối chiếu motif thực nghiệm, và kiểm chứng hạ nguồn.**

Tên tạm: *Dự đoán liên kết vị trí phospho – kinase trong điều kiện zero-shot cho dark kinome, dùng mô hình PLM điều kiện theo miền kinase, kèm tập dự đoán hợp quy (conformal) và đối chiếu XAI với motif đặc hiệu đo bằng thực nghiệm.*

- **Đầu vào:** một cặp (cửa sổ trình tự quanh vị trí phospho — thực tế là 15 amino acid, ±7; trình tự **miền kinase** của một kinase ứng viên).
- **Đầu ra:** điểm số cho cặp đó; gộp lại thành **xếp hạng các kinase ứng viên cho một vị trí**, kèm **tập dự đoán có bảo đảm phủ** ở mức tin cậy đặt trước (ví dụ "một trong 5 kinase này, bảo đảm phủ 90%") thay vì một dự đoán đơn lẻ.
- **Điểm mấu chốt:** kinase trong tập test **không xuất hiện trong tập huấn luyện** (zero-shot). Mô hình phải suy ra đặc hiệu cơ chất của một kinase **từ trình tự miền kinase của nó**, chứ không phải từ các vị trí đã gán nhãn cho chính nó. Đây là điều kiện bắt buộc nếu muốn nói gì về dark kinome.
- **Vì sao cần:** theo tài liệu DARKIN, **hơn 95% vị trí phospho đã phát hiện ở người chưa có chú giải kinase thượng nguồn** `[chưa kiểm — số dẫn lại từ tóm tắt bài DARKIN, cần đọc toàn văn để xác nhận]`. Người làm thực nghiệm muốn biết "nên knock down kinase nào để kiểm vị trí này" chứ không muốn một con số điểm tin cậy không hiệu chỉnh.

---

## 2. Dữ liệu: đã tải và đếm thật, không phải suy đoán

Quy tắc của dự án là kiểm dữ liệu thật trước khi kết luận khả thi. Đã làm trong phiên này.

**Benchmark DARKIN**, repo công khai `tastanlab/darkin`, clone được từ môi trường cloud (41 MB) `[tự đo]`. Bài: *DARKIN: a zero-shot benchmark for phosphosite–dark kinase association using protein language models*, **Bioinformatics 2025, 41(11)** `[chưa kiểm — chỉ thấy qua tóm tắt]`; bản workshop sớm hơn ở ICLR 2024.

Split mặc định (`split1___random_seed_12345`, chế độ ZSL) `[tự đo]`:

| Tập | Số vị trí | Số cặp (vị trí–kinase) | Số kinase | Số vị trí/kinase (min · trung vị · max) |
|---|---|---|---|---|
| Train | 8.559 | 11.473 | 308 | 1 · 6 · 949 |
| Validation | 1.484 | 1.628 | 46 | 10 · 15 · 486 |
| Test | 1.414 | 1.615 | **38** | **14** · 27 · 213 |

Ba điều số liệu này nói ra:

1. **Tập kinase của ba tập là rời nhau**, và tài liệu của họ ghi rõ ba nguyên tắc chia: ngưỡng tối thiểu số vị trí để một kinase được vào test/validation, phân tầng theo **nhóm kinase**, và **kinase có đồng dạng miền trên ngưỡng thì bị buộc vào cùng một tập** — tức là **kiểm soát rò rỉ ở mức đồng dạng đã nằm trong thiết kế benchmark**, không phải việc sinh viên phải tự dựng. Đây chính là thứ đã mất rất nhiều công ở hướng RTK–ATP và ở hướng sirtuin.
2. **Mọi kinase trong test có ít nhất 14 vị trí** nên chỉ số từng kinase không dựa trên 2–4 điểm dữ liệu — đúng chỗ mà [khảo sát sirtuin](sirtuin-substrate-deep-research.md) đã phải bỏ các con số của SIRT6/SIRT7 vì chỉ có 2 và 4 dương tính.
3. Có **5 split theo seed khác nhau** trong repo (0, 42, 87, 1001, 12345) cộng script tự sinh split mới `[tự đo]`, nên báo được **khoảng tin cậy qua nhiều split**, không chỉ một con số.

**Đặc trưng phía kinase cũng có sẵn offline:** `Darkin_Dataset/data_files/kinase_properties.csv` có **392 kinase**, mỗi dòng gồm `Kinase_Domain` (trình tự miền kinase), `Family`, `Group`, `active_site` và một số embedding sẵn `[tự đo]`. Nghĩa là phần "điều kiện theo kinase" không cần tải thêm gì.

**Baseline đã công bố, và cố tình đơn giản:** bài DARKIN đánh giá các PLM (ESM, ProtT5-XL, SaProt) bằng **k-NN không cần huấn luyện** và một **bộ phân loại bilinear** `[chưa kiểm]`. Đây là baseline *khảo sát PLM*, không phải mô hình được tối ưu cho bài toán — tức là còn nhiều khoảng trống cho tiêu chí 2.

---

## 3. Chấm theo năm tiêu chí

| Tiêu chí | Đề tài này | Căn cứ |
|---|---|---|
| 1. Tính mới của hướng | **Mạnh** | Bài toán được chính tài liệu benchmark tuyên bố là chưa giải được; >95% vị trí phospho chưa có kinase thượng nguồn. Phần mới của luận văn **không phải** "chưa ai làm dark kinome" (đã có người làm) mà là *kiểm chứng hạ nguồn* ở mục dưới |
| 2. Đề xuất/cải tiến phương pháp | **Mạnh** | Baseline hiện tại là k-NN và bilinear. Có ít nhất ba trục cải tiến cụ thể, kiểm được bằng ablation: cross-attention giữa biểu diễn miền kinase và cửa sổ vị trí thay cho tích bilinear; học đa nhiệm với PSSM đặc hiệu đo bằng thực nghiệm làm tín hiệu phụ; hàm mất mát nhận biết nhóm kinase (vì test được phân tầng theo nhóm) |
| 3. Phương pháp mới | **Mạnh** | Đúng mạch ví dụ GVHD đưa (PSSM → PLM): ở đây là PLM **theo cặp** có điều kiện, LoRA, và **conformal prediction** — phần bảo đảm thống kê thì GVHD chưa có công trình nào dùng, theo [danh mục đã tra](../../advisor/README.md) |
| 4. XAI | **Mạnh, và đo được** | Có **ground truth định lượng** cho phần giải thích: motif đặc hiệu của 303 kinase Ser/Thr (Johnson 2023, *Nature* 613:759–766) và 93 kinase Tyr (Yaron-Barir 2024, *Nature* 629:1174–1181) `[chưa kiểm toàn văn]`. Occlusion/attribution của mô hình **phải** chỉ đúng vị trí quyết định trong motif đó; dự án đã tự đo một ví dụ loại này (CDK: proline ở +1 có ở 83% dương tính so với 3% âm tính). Đây là **kiểm tra tính trung thực của giải thích**, mạnh hơn hẳn việc vẽ heatmap rồi kể chuyện |
| 5. Ứng dụng/website | **Mạnh, có người dùng thật** | Nhập một vị trí phospho (hoặc dán một protein) → trả về xếp hạng kinase ứng viên **kèm tập có bảo đảm phủ** và phần giải thích motif. Quyết định mà người dùng đưa ra sau đó là cụ thể: knock down kinase nào để kiểm. Có thể so trực tiếp với các web tool hiện có |

**Đóng góp làm nên tính mới ở tiêu chí 1 — nói cho đúng:** không phải "đầu tiên dự đoán dark kinase". Đã có tiền lệ (mục 5). Phần chưa thấy ai làm là **kiểm chứng hạ nguồn**: lấy dự đoán ở mức từng vị trí, đưa vào bài toán **suy luận hoạt tính kinase** từ dữ liệu phosphoproteomics, và đo xem dự đoán tốt hơn ở mức vị trí có làm suy luận hoạt tính tốt hơn hay không. Có sẵn benchmark cho phần hạ nguồn: **benchmarKIN** (Müller-Dott và cs., *Nat Commun* 2025, 16:4771), và chính bài đó kết luận rằng **chọn thư viện kinase–cơ chất ảnh hưởng tới kết quả nhiều hơn chọn phương pháp suy luận** `[chưa kiểm toàn văn]`. Đó là một lập luận rất gọn: nếu thư viện quyết định kết quả, thì việc bù chỗ trống của thư viện bằng dự đoán zero-shot là việc **đáng đo**, và nó chưa được đo `[chưa tìm thấy, không kết luận là chưa từng có]`.

---

## 4. So với ứng viên đang dẫn đầu

Ứng viên dẫn đầu hiện tại trong repo là **benchmark chuyển miền SIRT1/2/3** ([topic-final-recommendation.md](topic-final-recommendation.md) sau đính chính 10/10/2026), dự phòng là **B — phospho theo nhóm kinase** ([b-method-layer-draft.md](b-method-layer-draft.md)).

| | Benchmark sirtuin SIRT1/2/3 | B (phospho theo nhóm kinase) | **Đề xuất mới (dark kinome)** |
|---|---|---|---|
| 1. Tính mới | Trung bình: tính mới sinh học đã hết (Deep-PLA 2020 phủ SIRT1/2/3/6/7); còn lại là "chưa ai đo lại" | Trung bình | **Mạnh**: bài toán mở, cộng kiểm chứng hạ nguồn chưa ai làm |
| 2. Cải tiến phương pháp | **Yếu**: sản phẩm là một phép đo, phần mô hình chỉ là thang baseline | Trung bình–mạnh | **Mạnh**: baseline công bố là k-NN/bilinear |
| 3. Phương pháp mới | Trung bình | Mạnh | **Mạnh** |
| 4. XAI | **Yếu**: sirtuin **không có** ground truth motif định lượng (đây đúng là lý do B thắng tiêu chí 4 trong đánh giá trước) | Mạnh (motif CDK) | **Mạnh**: ground truth cho 303+93 kinase |
| 5. Ứng dụng | Mỏng | Trung bình | **Mạnh** |
| Cổng dữ liệu | Phải tự dựng tập đánh giá trong tế bào từ 2–3 bài rời rạc | Chỉ có phía test, **không có split** chuẩn | **Benchmark có sẵn, split rời nhau, 5 seed, kiểm soát đồng dạng sẵn trong thiết kế** |
| Rủi ro lớn nhất | Phụ thuộc việc GVHD **chấp nhận một kết quả âm** làm đóng góp chính | Không có benchmark chuẩn để so | Cạnh tranh đông và mới (mục 5) |

**Kết luận so sánh:** đề tài sirtuin thắng ở chỗ nó là một câu hỏi khoa học sạch sẽ và sinh viên đã hiểu rất sâu, nhưng nó **chỉ mạnh ở một trong năm tiêu chí** (tính mới dạng "đo lại"), yếu ở tiêu chí 2 và 4, và đặt cược vào một câu hỏi mà chưa biết câu trả lời: GVHD có nhận kết quả âm làm đóng góp chính không. Đề xuất mới **đạt cả năm tiêu chí mà không cần cược nào**, vì đóng góp của nó là một mô hình tốt hơn trên một benchmark công khai, cộng một phép đo hạ nguồn, cộng một ứng dụng — ba thứ đều ra kết quả dương hoặc âm đều dùng được.

So với dự phòng B: đề xuất mới **là B được đặt đúng chỗ**. B có đúng ý tưởng (phospho, nhóm kinase, XAI đối chiếu motif, conformal) nhưng vấp ở chỗ benchmark dbPTM **không có split huấn luyện** nên phải tự dựng tập train từ OmniPath rồi tự lọc đồng dạng — một khối việc không ai kiểm chứng được. DARKIN cho đúng phần còn thiếu đó, và đổi bài toán từ "vị trí này có bị phospho không" (đã đông) sang "kinase nào phospho vị trí này, kể cả kinase chưa từng thấy" (khó hơn, giá trị hơn).

---

## 5. Tiền lệ: không được nói "đầu tiên"

Phải nêu đúng những công trình sau trong phần khảo sát, nếu không GVHD sẽ nêu:

| Công trình | Làm gì | Khoảng trống còn lại |
|---|---|---|
| **Phosformer** (2023, *Bioinformatics*, PMC9900213) | Transformer nhận cặp (kinase, peptide) không cần gióng hàng; học được motif đặc hiệu `[chưa kiểm toàn văn]` | Không đánh giá dưới điều kiện kinase rời nhau nghiêm ngặt; không có bảo đảm thống kê |
| **Phosformer-ST** (đa nhiệm, Ser/Thr) | Huấn luyện trên 303 kinase Ser/Thr đo bằng thư viện peptide tổ hợp; tuyên bố làm được zero-shot `[chưa kiểm]` | Mức "zero-shot" chưa đo trên split kiểm soát đồng dạng; chưa có kiểm chứng hạ nguồn |
| **DARKIN** (2025, *Bioinformatics* 41(11)) | Dựng chính benchmark này; đánh giá PLM bằng k-NN và bilinear | Baseline cố ý đơn giản; **đây là nền của đề tài, không phải đối thủ** |
| **Prot2Token** (bioRxiv 2024.05.31.596915; LMRL@ICLR 2025) | Khung token hóa đa nhiệm, có nhắc khả năng zero-shot cho dark kinase, nhưng bằng chứng được mô tả là sơ bộ `[chưa kiểm]` | Chưa báo chỉ số trên benchmark zero-shot chuẩn |
| **benchmarKIN** (2025, *Nat Commun* 16:4771) | Benchmark cho suy luận hoạt tính kinase; kết luận thư viện quan trọng hơn phương pháp `[chưa kiểm]` | Chưa ai đưa dự đoán zero-shot vào để bù chỗ trống của thư viện rồi đo lại |

Cách nói an toàn: *"bài toán này đã có người làm và chưa ai làm tốt; luận văn đóng góp một mô hình điều kiện theo kinase tốt hơn baseline của benchmark, cộng hai thứ chưa thấy trong các công trình trên: dự đoán có bảo đảm phủ, và kiểm chứng hạ nguồn bằng suy luận hoạt tính kinase."*

---

## 6. Ràng buộc nào được bỏ đã làm đề xuất khác đi

Nói rõ để sinh viên thấy đề xuất này **không áp dụng được nguyên trạng** khi các ràng buộc quay lại:

| Ràng buộc được bỏ | Nếu còn ràng buộc thì sao |
|---|---|
| **Độ liên quan tới GVHD** | Đây là thay đổi lớn nhất. Hướng này **rời hẳn** sirtuin/HDAC và PLM–mCNN trên trình tự — tức là rời khỏi nhánh GVHD đã công bố. Được lợi: tính mới không bị Deep-PLA/DeepSIRT ăn trước. Mất: GVHD khó phản biện sâu giúp, và phải tự lập luận thang đóng góp |
| **Thời gian** | Bốn phần (mô hình + conformal + XAI đối chiếu + web) cộng kiểm chứng hạ nguồn **không vừa 8–9 tuần**. Nếu mốc tuần 14–15 còn hiệu lực, phải cắt: giữ mô hình + XAI + web, bỏ phần hạ nguồn benchmarKIN sang "hướng mở rộng" |
| **GPU** | Mô hình theo cặp trên 11.473 cặp × nhiều split × ablation là tải GPU thật, cộng fine-tune LoRA. Không có GPU thì phải lùi về PLM đóng băng + đầu nhẹ, và lúc đó tiêu chí 2 yếu đi |
| **Lĩnh vực** | Không ảnh hưởng nhiều: vẫn là PTM trên trình tự protein, vẫn là tin sinh |

---

## 7. Việc phải kiểm trước khi coi đây là đề tài (chưa làm)

1. **Đọc toàn văn bài DARKIN** để xác nhận: chỉ số họ dùng (có MCC/AUPRC hay không), con số baseline của ESM/ProtT5/SaProt, và con số ">95% vị trí chưa có chú giải".
2. **Đọc Phosformer-ST** để biết chính xác nó đã đo zero-shot thế nào — đây là đối thủ gần nhất, và nếu nó đã đo trên split kiểu DARKIN thì phần "cải tiến phương pháp" phải viết lại.
3. **Kiểm tải được PSSM đặc hiệu của Johnson 2023 / Yaron-Barir 2024** từ môi trường này (ground truth cho tiêu chí 4). Nếu không tải được, phương án dự phòng là tự đo motif từ chính tập train theo nhóm kinase — dự án đã làm được việc này một lần (CDK proline +1).
4. **Chạy lại baseline k-NN của DARKIN** trên split mặc định để có một con số gốc tự kiểm, trước khi hứa cải tiến được bao nhiêu.
5. **Kiểm benchmarKIN** có cho phép thay thư viện kinase–cơ chất bằng thư viện do mình dự đoán hay không — nếu không, phần kiểm chứng hạ nguồn mất chỗ dựa và tính mới ở tiêu chí 1 yếu đi đáng kể.

## 8. Câu hỏi cho GVHD nếu mang hướng này ra

1. Hướng này không nằm trong nhánh thầy đã công bố — thầy có nhận hướng dẫn một đề tài như vậy không, hay nên giữ trong nhánh PTM/sirtuin?
2. Với một bài toán đã có benchmark công khai và baseline công bố, mức cải tiến bao nhiêu thì thầy coi là đủ cho tiêu chí 2?
3. Phần bảo đảm thống kê (conformal) có được tính là "phương pháp mới" ở tiêu chí 3, hay thầy coi nó là kỹ thuật phụ?
4. Kiểm chứng hạ nguồn (dự đoán ở mức vị trí có cải thiện suy luận hoạt tính kinase hay không) có được tính là đóng góp riêng, hay chỉ là một thí nghiệm bổ sung?

---

## Tài liệu dẫn

- Năm tiêu chí: [docs/meeting/session-01-minutes.md](../../../meeting/session-01-minutes.md), mục 4.
- Ứng viên dẫn đầu và dự phòng: [topic-final-recommendation.md](topic-final-recommendation.md) · [b-method-layer-draft.md](b-method-layer-draft.md) · [sirtuin-substrate-deep-research.md](sirtuin-substrate-deep-research.md) · [compute-novelty-directions.md](compute-novelty-directions.md).
- DARKIN: repo `tastanlab/darkin`; bài trên *Bioinformatics* 2025, 41(11), PMC12579546; bản workshop ICLR 2024.
- Phosformer: *Bioinformatics* 2023, PMC9900213.
- Atlas đặc hiệu cơ chất: Johnson và cs., *Nature* 2023, 613(7945):759–766 (303 kinase Ser/Thr); Yaron-Barir và cs., *Nature* 2024, 629(8014):1174–1181 (93 kinase Tyr).
- benchmarKIN: Müller-Dott và cs., *Nat Commun* 2025, 16:4771, PMC12098709.
