# Tiền lệ cho cổng phơi lộ — tra ngày 14/10/2026

> Tra sau khi [architecture-check](README.md) đo được hiệu ứng phơi lộ. **Kết luận ngắn: tiền đề không mới,
> và hiện tượng đổi dấu cũng đã có người tìm ra trước.** Phần còn trống là **nơi đặt cổng** (bên trong mô
> hình, tại bước gộp) — chưa tìm được tiền lệ, nhưng đây là **"chưa tìm thấy"**, không phải "chưa ai làm".
> Báo cáo này sửa lại phần mục 1 của `README.md`, vốn gọi phép đo đó là "phép đo đầu tiên trong repo chứng
> minh nó" mà không đối chiếu y văn.

## Nhãn bằng chứng

- **[đã đọc]** đã đọc toàn văn hoặc phần Methods/Results liên quan.
- **[qua tóm tắt]** chỉ thấy qua tóm tắt tìm kiếm hoặc abstract — **chưa xác minh**.
- Theo quy ước của đề tài: **không** nói "chưa ai làm". Chỗ không tìm được tiền lệ thì ghi là chưa tìm thấy.

## 1. Tiền đề "tín hiệu degron phụ thuộc mức phơi lộ" — **đã được công bố nhiều lần**

| Công trình | Họ đã làm gì | Nhãn |
|---|---|---|
| **Voutsinos 2026** (*Sci Adv*), chính tác giả PAP | Fig 3: điểm degron so với rASA và pLDDT, **ρ = −0,47** trên 173 protein phơi lộ nhất. Fig 6: ΔPAP ở vùng phơi lộ, Kruskal–Wallis **P = 5,4 × 10⁻⁶**. Nói rõ: ở vùng phơi lộ và không có cấu trúc, độ mạnh degron **giải thích phần lớn** độ dồi dào của biến thể protein nguyên vẹn | **[đã đọc]** (ghi chú repo: [voutsinos-2026.md](../../../../lectures/papers/voutsinos-2026.md)) |
| **Larsen 2025** (bioRxiv, degron ở transcription factor) | Điểm degron so với rASA \|r\| = **0,41**; so pLDDT \|r\| = **0,36**, trên toàn thư viện. 6.992/21.970 degron (32%) có rASA > 0,7; 8.817 (40%) có pLDDT < 70 | **[đã đọc]** toàn văn phần kết quả |
| **QCDPred** (Johansson 2022/2023, cùng nhóm) | Degron chất lượng-kiểm soát giàu amino acid kỵ nước, **đúng kỳ vọng rằng chúng bị chôn trong protein gấp đúng**; báo tương quan giữa độ dồi dào và tiềm năng degron **ở vùng vô định hình** | **[qua tóm tắt]** |
| **DEGRONOPEDIA** (*NAR* 2024) | Tích hợp sẵn **mô hình hóa khả năng tiếp cận dung môi** và mô phỏng phân giải; tính cấu trúc bậc hai và rASA cho **từng motif degron** | **[qua tóm tắt]** |
| **JoGo degron viewer** | Phân loại bối cảnh cấu trúc của biến thể bằng **đúng tổ hợp rASA + pLDDT**: "functional" nếu rASA ≥ 0,25 và (disorder hoặc pLDDT < 70); "exposed" nếu rASA ≥ 0,25 và có cấu trúc; "buried" nếu rASA < 0,25 | **[qua tóm tắt]** |

**[phân tích]** Tiền đề của thành phần 4 là **kiến thức đã xác lập trong chính nhóm tác giả PAP**, không phải
phát hiện. Ghi chú repo [larsen-2025.md](../../../../lectures/papers/larsen-2025.md) đã nói
"họ đã dùng cấu trúc, đã tính rASA và pLDDT" — nhưng mục 1 của `README.md` vẫn viết như thể phép đo của
phiên 14/10 là phép đo đầu tiên chứng minh tiền đề. **Câu đó sai và đã được sửa.**

## 2. Hiện tượng ΔPAP **đổi dấu** giữa vùng chôn và vùng phơi lộ — **Larsen 2025 đã tìm ra**

Đây là điều chỉnh quan trọng nhất của lần tra này. Phiên 14/10 đo được ΔPAP tương quan **−0,1928** ở
residue chôn và **+0,3733** ở residue phơi lộ, rồi gọi đó là "một lỗi hệ thống mà cổng phơi lộ sửa".

**Larsen 2025 đã báo đúng hiện tượng này**, trên protein CRX, tách theo vùng: **[đã đọc]**

| Vùng CRX | ΔPAP | ESM-1b |
|---|---:|---:|
| Vùng vô định hình (IDR) | Pearson **0,54** | 0,31 |
| Homeodomain đã gấp | Pearson **−0,19** | 0,52 |

**[phân tích]** Dấu đảo từ +0,54 sang **−0,19**, cùng chiều và cùng độ lớn với phép đo của phiên 14/10.
Khác biệt: họ dùng **một** protein và nhãn **transactivation** (không phải độ dồi dào), và chính họ ghi là
"khó tách ảnh hưởng lên độ dồi dào khỏi chức năng nội tại". Phép đo của repo dùng **6 protein, 33.718 biến
thể, nhãn độ dồi dào trực tiếp**, nên là một **xác nhận lại ở quy mô lớn hơn trên nhãn sạch hơn**, không
phải phát hiện mới. Phải phát biểu đúng như vậy trong đề cương và luận văn.

## 3. Tiền lệ sát nhất về phương pháp: **Schulze & Lindorff-Larsen, eLife 2026** — và nó là baseline bắt buộc

**[đã đọc]** toàn văn (PMC13218725). Theo PubMed: [10.7554/eLife.103721](https://doi.org/10.7554/eLife.103721).
Cùng nhóm Lindorff-Larsen với Voutsinos và QCDPred, công bố **28/05/2026**.

| Họ làm | Phiên 14/10 làm |
|---|---|
| Gộp **6 thí nghiệm VAMP-seq**, **31.614** điểm biến thể | Gộp 6 bộ độ dồi dào MaveDB, **33.718** biến thể khớp cấu trúc |
| Đúng **cùng 6 protein**: PTEN, TPMT, NUDT15, CYP2C9, ASPA, PRKN | 6 protein đó **cộng GCK** (và CYP2C19 bị loại) |
| Tách residue thành **chôn / phơi lộ**, ngưỡng rASA **0,1** chọn bằng grid search tối đa hóa Pearson LOPO-CV | Chia 4 khoảng rASA (0,2 / 0,5 / 0,7), **không tối ưu ngưỡng** |
| Dựng **ma trận thay thế** riêng cho mỗi lớp, đánh giá bằng leave-one-protein-out | Không dựng ma trận; chỉ đo tương quan của ΔPAP |
| Dùng **cấu trúc thực nghiệm**, và **homodimer** cho NUDT15 và ASPA | Dùng **AlphaFold monomer** cho tất cả |
| Thêm **WCN** (weighted contact number) vì rASA không phân giải được bên trong lõi | Không dùng WCN |
| Đối chứng **ThermoMPNN ΔΔG** | Không có đối chứng ΔΔG |

**Bốn hệ quả cho đề tài — [phân tích]:**

1. **Có một baseline mạnh hơn mà đề tài chưa tính tới.** rASA **một mình** đã cho Spearman **0,45** trung
   bình (0,54 nếu bỏ ASPA) với điểm độ dồi dào. ΔPAP của phiên 14/10 chỉ đạt 0,3733 **ở khoảng phơi lộ
   nhất**. Nếu luận văn muốn dùng nhãn độ dồi dào ở bất kỳ vai trò nào thì **ma trận thay thế theo lớp
   phơi lộ của Schulze 2026 và ThermoMPNN ΔΔG là hai đối chứng bắt buộc**, không phải tùy chọn. Chính các
   tác giả đề nghị dùng ma trận của họ làm "strong baseline cho việc phát triển mô hình độ dồi dào sau này".
2. **Một lỗi phương pháp của phiên 14/10 đã lộ ra.** Họ dùng **homodimer** cho NUDT15 và ASPA, vì rASA tính
   trên monomer **phân loại sai** các residue ở mặt tiếp xúc (tưởng phơi lộ trong khi thực tế bị che). Phiên
   14/10 dùng AlphaFold monomer cho cả 8 protein, nên **rASA của NUDT15 và ASPA bị lệch về phía phơi lộ**.
   Cần chạy lại với cấu trúc dimer cho hai protein đó trước khi dùng con số nào vào tài liệu.
3. **GCK không nên nằm trong tập.** Bộ GCK mà phiên 14/10 dùng (`urn:mavedb:00000096-b-1`) đo bằng
   **DHFR-PCA**, không phải VAMP-seq. Schulze 2026 loại GCK để giữ **một phenotype duy nhất**. Trộn hai loại
   assay là đúng thứ bài báo cảnh báo. Phải chạy lại không có GCK.
4. **Nhưng khoảng trống mà họ tự nêu lại đúng là hướng của đề tài.** Họ ghi rõ framework cấu trúc đơn giản
   của họ **không bắt được** các cơ chế cần máy phân hủy, trong đó có **neo-degron ở vị trí phơi lộ**, và
   nói các chỗ lệch đó "có thể dùng để định hướng phát triển mô hình độ dồi dào sau này, ví dụ bằng cách
   đưa vào đặc trưng sinh hóa phức tạp hơn". Họ còn nêu ca cụ thể: **S109 của PRKN**, một residue phơi lộ có
   profile thay thế giống residue chôn, được cho là tạo **degron chất lượng-kiểm soát phơi lộ** khi đột biến.
   Đây là **lời mời trực tiếp** cho đúng loại mô hình mà đề tài đề xuất, và là một câu dẫn nhập mạnh cho
   đề cương.

## 4. Nơi đặt cổng bên trong mô hình — **chưa tìm thấy tiền lệ**

Phát biểu của đề tài (topic-decision §5) là "mới ở **nơi đặt** cổng phơi lộ — tại
bước gộp, không phải đầu vào". Tra lần này **không tìm được** tiền lệ, và tìm được bằng chứng ngược lại
rằng các mô hình degron hiện có đều **không** làm thế:

| Mô hình | Cấu trúc vào mô hình thế nào | Nhãn |
|---|---|---|
| **PAP** (Voutsinos 2026) | **Không vào mô hình.** rASA và pLDDT chỉ dùng cho phân tích sau | **[đã đọc]** mã nguồn đầy đủ, [voutsinos-2026-audit](../voutsinos-2026-audit/README.md) |
| **MetaDegron** (*Brief Bioinform* 2024) | Khả năng tiếp cận dung môi (Spider2) là **đặc trưng đầu vào của nhánh XGBoost** (MetaDegron-X). Nhánh học sâu (MetaDegron-D) chỉ dùng **trình tự** (SeqVec). **Không có attention**, chỉ max-pooling. **Không gate theo khả năng tiếp cận** | **[đã đọc]** phần Methods |
| **DEGRONOPEDIA** | Mô hình hóa khả năng tiếp cận dung môi như **bước phân tích/annotation** quanh motif | **[qua tóm tắt]** |
| **Schulze 2026** | Cấu trúc dùng để **chia lớp** residue trước khi tra ma trận; không phải mô hình học được | **[đã đọc]** |
| **BioBlobs** (10/2025) | Attention-MIL có cổng trên **substructure** của protein — nhưng là phương pháp **không giám sát** cho dự đoán chức năng, **không** dùng khả năng tiếp cận dung môi | **[qua tóm tắt]** |
| **Ilse 2018** | Nguồn gốc của "gated attention" trong MIL; cổng là **tanh × sigmoid trên đặc trưng thể hiện**, không phải cổng theo đại lượng cấu trúc bên ngoài | **[qua tóm tắt]** |

**[phân tích]** Phát biểu đúng mức, dùng được trong đề cương: cấu trúc đã được dùng rộng rãi trong dự đoán
degron, nhưng theo ba cách — phân tích sau (PAP, DEGRONOPEDIA), đặc trưng đầu vào của một nhánh phi học sâu
(MetaDegron-X), hoặc biến chia lớp (Schulze 2026). **Chưa tìm thấy** mô hình degron nào dùng đại lượng phơi
lộ để **điều biến trọng số gộp** của một mô hình học được mức residue. Vẫn giữ nguyên quy ước: đây là chưa
tìm thấy sau một lần tra, **không** phải bằng chứng chưa ai làm, và tính mới của đề tài **không nên** dựa
chính vào điểm này.

## 5. Việc phải làm vì lần tra này

1. **Chạy lại phần 1 của [architecture-check](README.md)** với ba sửa: bỏ GCK (không phải VAMP-seq), dùng
   cấu trúc **homodimer** cho NUDT15 và ASPA, và thêm ngưỡng rASA **0,1** của Schulze 2026 bên cạnh các
   khoảng hiện có. Trước khi làm xong, **không** dùng con số +0,6625 trong tài liệu nào.
2. **Thêm hai đối chứng bắt buộc** vào thiết kế benchmark: ma trận thay thế theo lớp phơi lộ (Schulze 2026)
   và ThermoMPNN ΔΔG — nhưng chỉ cho phần nào của đề tài dùng nhãn độ dồi dào protein nguyên vẹn.
3. **Sửa phát biểu trong mọi tài liệu**: hiệu ứng phơi lộ và hiện tượng đổi dấu là **xác nhận lại** Larsen
   2025 và Voutsinos 2026 ở quy mô lớn hơn, không phải phát hiện của đề tài.
4. **Dùng câu của Schulze 2026 làm dẫn nhập**: chính nhóm mạnh nhất trong lĩnh vực nói framework cấu trúc
   của họ bỏ sót neo-degron và mời phát triển tiếp. Kèm ca **PRKN S109**.
5. Đọc toàn văn **QCDPred**, **DEGRONOPEDIA** và **JoGo** để nâng ba dòng **[qua tóm tắt]** lên **[đã đọc]**
   trước khi viết tổng quan tài liệu.

## Nguồn

- [A near-complete map of human cytosolic degrons and their relevance for disease](https://www.science.org/doi/10.1126/sciadv.adz3483) — Voutsinos 2026, *Sci Adv* (trang trả 403 từ mạng này; số liệu lấy từ ghi chú repo đã đọc trước đó và từ bản bioRxiv)
- [Comprehensive degron mapping in human transcription factors](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full) — Larsen 2025, bioRxiv
- [Effects of residue substitutions on the cellular abundance of proteins](https://doi.org/10.7554/eLife.103721) — Schulze & Lindorff-Larsen, *eLife* 2026 (tra qua PubMed, PMID 42207673)
- [Prediction of quality-control degradation signals in yeast proteins](https://consensus.app/papers/details/3b61bd83d7c052f8960847a6a08edd25/?utm_source=claude_code) — Johansson 2022, QCDPred
- [DEGRONOPEDIA: A practical guide to identifying and targeting protein degrons](https://consensus.app/papers/details/604fb5847bc153cd9984e842a8b93f2e/?utm_source=claude_code) — Szulc 2025
- [MetaDegron: multimodal feature-integrated protein language model](https://academic.oup.com/bib/article/25/6/bbae519/7828723) — *Brief Bioinform* 2024
- [Systematic prediction of degrons and E3 ubiquitin ligase binding via deep learning](https://consensus.app/papers/details/b575330884e15964ae56a136e49c0fc6/?utm_source=claude_code) — Degpred, Hou 2022
- [Degron Variation viewer](https://jogo.csml.org/degron-static/degron_interesting.html) — JoGo
- [BioBlobs](https://arxiv.org/pdf/2510.01632) · [Attention-based Deep MIL](https://arxiv.org/pdf/1802.04712) — Ilse 2018
- [DEGRONOPEDIA documentation](https://degronopedia.com/degronopedia/documentation)
