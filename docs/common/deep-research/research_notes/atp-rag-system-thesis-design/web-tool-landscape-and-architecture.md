# Bối cảnh web server / công cụ phần mềm cho dự đoán vị trí gắn ligand ở protein (góc nhìn sản phẩm phần mềm)

> Phạm vi: **chỉ bàn mặt sản phẩm phần mềm** (deploy, I/O, API, UI, giấy phép, bảo trì, venue công bố, kiến trúc tham chiếu). Không đánh giá mô hình/ML — người khác phụ trách.
> Thời điểm kiểm chứng: **01/10/2026**. Mọi lần kiểm liveness đều bằng `curl -L --max-time 20` và GitHub REST API trong phiên này.
> Quy ước nhãn: **đã kiểm** = đọc trực tiếp trong nguồn có link; **suy luận** = tôi diễn giải từ các dữ kiện đã kiểm.

---

## KQ1. Những web server / công cụ nào đang tồn tại cho dự đoán residue gắn ligand/cofactor từ sequence?

### Takeaway

Niche này có rất nhiều bài báo nhưng **rất ít sản phẩm còn sống và được bảo trì**: tính đến 01/10/2026 chỉ `prankweb.cz` (structure-based) và `GPSite` (sequence-based, multi-ligand, có ATP) là web server còn chạy và có hệ sinh thái phần mềm tử tế; **PredictProtein — cửa ngõ chính của bindEmbed21 — đã sập từ 12/05/2025 và chính Rostlab nói "không rõ có phục hồi được không"**; PUResNet, ScanNet, DeepFRI không còn endpoint web sống. Không có một web server nào còn sống chuyên biệt cho **ATP + sequence-only** ngoài GPSite (đa ligand) và ATPbind (bắt buộc structure, trả kết quả qua email).

### Cited Findings

**Kết quả kiểm liveness trực tiếp (đã kiểm, chạy 01/10/2026)**

| Công cụ | URL kiểm | HTTP | Nhận xét |
|---|---|---|---|
| GPSite | https://bio-web1.nscc-gz.cn/app/GPSite | **200** (2,65 s) | Sống. SPA (HTML rỗng, render bằng JS; dùng `pdbe-molstar-plugin-1.2.1.js` → có viewer 3D nhúng) |
| LMetalSite | https://bio-web1.nscc-gz.cn/app/LMetalSite | **200** (0,59 s) | Sống, cùng hạ tầng NSCC-GZ |
| PrankWeb / P2Rank | https://prankweb.cz/ | **200** | Sống |
| ATPbind | https://zhanggroup.org/ATPbind/ | **200** | Sống |
| ATPbind (mirror UMich) | https://seq2fun.dcmb.med.umich.edu//ATPbind/ | **200** | Sống |
| COACH | https://zhanggroup.org/COACH/ | **200** | Sống |
| COFACTOR | https://zhanggroup.org/COFACTOR/ | **200** | Sống |
| TM-SITE (standalone page) | https://zhanggroup.org/TM-SITE/ | **404** | Link con đã mục, dù site gốc sống |
| PredictProtein | https://predictprotein.org/ | 200 nhưng **redirect sang `status.predictprotein.org`** | **Đã sập** (xem dưới) |
| LambdaPP | https://lambda.predictprotein.org/ → `lambda.rostlab.org` | 200 (trang thông báo) | **Backend defunct** (xem dưới) |
| Biocentral | https://biocentral.cloud/ | 200 | Sống (thay thế được Rostlab đề xuất) |
| NsitePred | http://biomine.cs.vcu.edu/servers/NsitePred/ | 200 nhưng redirect sang `server-handler/?type=servers&target=NsitePred/` | Chưa xác nhận form còn chạy; subdomain `nsitepred.biomine.cs.vcu.edu` = **000 (không kết nối)** |
| PUResNet | http://bioinfo.konkuk.ac.kr/PUResNet/ → `:8443/PUResNet/` | **404** | **Chết** |
| ScanNet | https://www.scanneteam.com/ | **000** | **Chết** (DNS/kết nối thất bại) |
| ScanNet (mirror LiU) | http://bioinfo.ifm.liu.se/ScanNet/ | **404** | **Chết** |
| DeepFRI | https://beta.deepfri.flatironinstitute.org/ | **000** | **Chết** |
| Seq2Bind | https://agrivax.onrender.com/seq2bind/scan | **200** | Sống (host trên Render) |
| bio.tools registry | https://bio.tools/ | 200 | Sống; có mục `bio.tools/bindembed21` (200) |

**Mức bảo trì mã nguồn (GitHub API, đã kiểm 01/10/2026)**

| Repo | `pushed_at` | Stars | Open issues | License |
|---|---|---|---|---|
| `rdk/p2rank` | **2026-09-11** | 464 | 15 | có |
| `cusbg/p2rank-framework` | **2026-02-11** | 14 | 0 | **null (không có license)** |
| `biomed-AI/LMetalSite` | **2025-10-23** | 19 | 1 | có |
| `Rostlab/bindPredict` | **2025-09-02** | 37 | 2 | có |
| `jertubiana/ScanNet` | 2025-06-18 | 147 | 3 | có |
| `jivankandel/PUResNet` | 2024-09-23 | 52 | 0 | **null** |
| `biomed-AI/GPSite` | 2024-08-29 | 31 | 0 | có |
| `flatironinstitute/DeepFRI` | **2023-03-24** | 356 | **34** | có |

**PredictProtein đã sập**
- Trang status (đọc trực tiếp): dịch vụ **DOWN**, thông báo đăng **12/05/2025**, "major technical issue", và nguyên văn "**it is unclear if the hosted service will be recoverable**"; hướng người dùng sang Biocentral và sang giao diện single-sequence mới đang phát triển tại `lambda.predictprotein.org`; liên hệ help@predictprotein.org — [status.predictprotein.org](https://status.predictprotein.org/) (đã kiểm)
- LambdaPP (`lambda.rostlab.org`): "**λPP's backend is currently defunct**" do **bio_embeddings hết hỗ trợ**; mục tiêu phục hồi tháng 9/2025; tích hợp Biocentral "underway" tính tới 02/2026 — [lambda.rostlab.org](https://lambda.rostlab.org/) (đã kiểm). Nghĩa là tới 10/2026 vẫn chưa có giao diện web sống cho bindEmbed21.

**bindEmbed21 / bindPredict (Rostlab)**
- Dự đoán residue gắn **metal ion, nucleic acid, small molecule** (3 lớp ligand, **không tách riêng ATP**); gồm `bindEmbed21DL` (ProtT5 → CNN 2 lớp) + `bindEmbed21HBI` (homology-based inference bằng MMseqs2) — [Nature Sci Rep 2021](https://www.nature.com/articles/s41598-021-03431-4), [PMC8668950](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/) (đã kiểm)
- **Runtime**: "generating binding residue predictions for one protein sequence took around 0.2 s" — [PMC8668950](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/) (đã kiểm)
- **Không có web server riêng**: "All data, the source code, and the trained model are available via GitHub (https://github.com/Rostlab/bindPredict)… bindEmbed21 and its components… are publicly available through bio_embeddings" — [PMC8668950](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/) (đã kiểm). Tức sản phẩm = **library + script**, phần "web" phụ thuộc PredictProtein/LambdaPP (đều đang sập).
- Giấy phép bài báo CC BY 4.0; repo `Rostlab/bindPredict` có file license (đã kiểm qua GitHub API).

**GPSite**
- Dự đoán đồng thời residue gắn **10 loại phân tử: DNA, RNA, peptide, protein, ATP, HEM và các ion kim loại**, multi-task, **không cần MSA hay structure thực nghiệm** (dùng embedding PLM + structure dự đoán bởi ESMFold) — [PMC11023698](https://pmc.ncbi.nlm.nih.gov/articles/PMC11023698/) (đã kiểm). **Đây là đối thủ trực tiếp gần nhất của đề tài: nó đã có nhãn ATP và đã có web server sống.**
- Có **cơ sở dữ liệu tiền tính toàn bộ Swiss-Prot**: "All ESMFold-predicted structures accompanied by the binding site annotations for Swiss-Prot are freely available in our user-friendly GPSiteDB database" — [GPSiteDB](https://bio-web1.nscc-gz.cn/database/GPSiteDB), [PMC11023698](https://pmc.ncbi.nlm.nih.gov/articles/PMC11023698/) (đã kiểm)
- Có **điểm mức protein**: "a protein-level binding score indicating the overall binding propensity to a specific ligand by averaging the top k predicted scores among all residues" — [PMC11023698](https://pmc.ncbi.nlm.nih.gov/articles/PMC11023698/) (đã kiểm)
- Bài báo **không tài liệu hóa**: giới hạn batch, tham số hàng đợi job, định dạng input cụ thể, khả năng viewer 3D, tài liệu API, thời gian chạy ước tính, hay license của web server — [PMC11023698](https://pmc.ncbi.nlm.nih.gov/articles/PMC11023698/) (đã kiểm: fetch toàn văn không tìm thấy các mục này)
- Có bản "protocol chapter" riêng mô tả server: [Springer Methods in Molecular Biology, "An Online Server for Geometry-Aware Protein Function Annotations Through Predicted Structure"](https://link.springer.com/protocol/10.1007/978-1-0716-4662-5_11) (đã kiểm sự tồn tại; **chưa đọc toàn văn** — paywall)

**ATPbind / ATPseq (Zhang group) — đặc tả sản phẩm, đọc trực tiếp từ HTML trang server**
- Là **meta-server**: "Starting from given **structure** of query protein, ATPbind will identify the ATP-binding sites by using SVM to integrate the outputs of two template-based predictors, i.e., S-SITEatp… and TM-SITEatp…, and three discriminative sequence-driven features, i.e., PSSM, predicted secondary structure, and predicted solvent accessibility" — [zhanggroup.org/ATPbind](https://zhanggroup.org/ATPbind/) (đã kiểm, scrape HTML)
- **Nếu input là sequence**: "I-TASSER will be used to generate 3D model first… If the input is a sequence, we strongly suggest users to employ the I-TASSER server to model the 3D structure first, **since the I-TASSER server used in ATPbind is not the newest one**" — [zhanggroup.org/ATPbind](https://zhanggroup.org/ATPbind/) (đã kiểm). Đây là một **debt kỹ thuật được chính tác giả thừa nhận trên trang sản phẩm**.
- **Email là bắt buộc**: form có trường "Email: (Mandatory, where results will be sent to)" → mô hình **asynchronous, trả kết quả qua email**, không có URL kết quả bền (đã kiểm, scrape HTML)
- Có module hậu xử lý **PocHunter** để cluster pocket từ residue đã dự đoán; có "[List the benchmark dataset] [Download the benchmark dataset]"; bản standalone qua **I-TASSER Suite / COACH Package** (đã kiểm, scrape HTML)
- ATPseq (thành phần sequence-only) được báo cáo accuracy 97,27%, sensitivity 57,52%, AUC 0,913 — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0003269721001421) (đã kiểm qua snippet, **không đọc toàn văn**)

**PrankWeb / P2Rank (structure-based, nhưng là kiến trúc tham chiếu tốt nhất)** — xem chi tiết ở KQ4.

**Các công cụ mới 2025–2026 tìm được**
- **Seq2Bind** — NAR Genomics and Bioinformatics **7(4):lqaf154, công bố 22/11/2025**. Dự đoán binding affinity protein–protein + **alanine mutation scanning** để xếp hạng interface residue, từ sequence. Cho người dùng **chọn 1 trong 4 model** (ProtBERT, ProtT5, ESM2, BiLSTM). Host tại `agrivax.onrender.com/seq2bind/scan` (phần của "StructF-suite"); **source code + pretrained model phát hành qua Google Colab**; CC-BY 4.0; đánh giá bằng "N-factor metric" ở N=1,2,3 — [PMC12639246](https://pmc.ncbi.nlm.nih.gov/articles/PMC12639246/) (đã kiểm)
- **PROBind** — "A Web Server for Prediction, Analysis and Visualization of Protein-Protein and Protein-Nucleic Acid Binding Residues", bioRxiv 2025.02.08.637237 — [bioRxiv PDF](https://www.biorxiv.org/content/10.1101/2025.02.08.637237.full.pdf) (đã kiểm tiêu đề qua search; **chưa đọc toàn văn, chưa kiểm liveness**)
- **BindWeb** — "A web server for ligand binding residue and pocket prediction from protein structures" — [PMC9667820](https://pmc.ncbi.nlm.nih.gov/articles/PMC9667820/) (đã kiểm tiêu đề; chưa đọc toàn văn)
- **S-DCNN** (ATP binding residue, CNN + SMOTE) — [PMC11744016](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11744016/) và **DeepATPseq-like ensemble CNN+LightGBM** — [PMC7832895](https://pmc.ncbi.nlm.nih.gov/articles/PMC7832895) (đã kiểm tiêu đề; **đều là bài method, không rõ có web server**)

### Inferences

- **suy luận**: Trong niche "ATP-binding residue từ sequence", **không tồn tại web server nào còn sống, có UI hiện đại, sequence-only và chuyên ATP**. GPSite che phủ ATP nhưng là multi-task tổng quát và không chuyên hoá theo họ protein; ATPbind chuyên ATP nhưng đòi structure + email + dựa trên I-TASSER cũ. Đây là **khoảng trống sản phẩm thực sự** cho một đề tài hướng tool, độc lập với việc mô hình có mới hay không.
- **suy luận**: Mẫu hình thất bại rõ nhất không phải "mô hình kém" mà là **phụ thuộc một dependency/host duy nhất**: bindEmbed21 mất mặt web vì `bio_embeddings` hết hỗ trợ và PredictProtein sập; PUResNet/ScanNet/DeepFRI mất endpoint vì host cá nhân/lab. Ngược lại P2Rank sống vì **CLI + Docker + framework tách rời web**.
- **suy luận**: `cusbg/p2rank-framework` và `jivankandel/PUResNet` **không có LICENSE file** → về mặt pháp lý là "all rights reserved", không đạt tiêu chí JOSS và gây rủi ro khi tái sử dụng. Đây là lỗi dễ tránh mà đề tài nên tránh ngay từ đầu.

### Gaps

- **ATPsite, TargetATPsite, E-pTool**: tôi **không tìm được** trang web hay bài báo chính thống nào trong các truy vấn đã thực hiện. Cần tra riêng từng cái; rất có thể URL đã mục (các công cụ này thuộc thế hệ 2010–2013).
- **NsitePred**: trang redirect sang `server-handler` của biomine; **không xác nhận được form submit còn hoạt động**. Cần mở trình duyệt thật.
- **ScanNet**: GitHub còn sống (commit 06/2025) nhưng cả hai URL web đều chết; **chưa tìm được URL web hiện hành** (có thể đã dời host).
- Không kiểm được **giấy phép và điều khoản sử dụng của web server GPSite** (chỉ có license của repo code).
- Không đọc được toàn văn chương Springer về GPSite server (paywall) → thiếu đặc tả batch/API chính xác.

---

## KQ2. Những công cụ này KHÔNG làm gì? (4 khoảng trống cụ thể)

### Takeaway

Cả bốn tính năng người hỏi nêu đều **thiếu một cách hệ thống**: không công cụ nào trong niche này báo cáo confidence đã calibrate hay cờ out-of-distribution; không công cụ nào hiển thị homolog gần nhất đã dùng để suy ra dự đoán (dù bindEmbed21HBI và ATPbind đều chạy trên homology/template); không công cụ nào sinh giải thích ngôn ngữ tự nhiên có dẫn nguồn; và không công cụ nào cho phép cập nhật/đổi phiên bản reference database mà không huấn luyện lại.

### Cited Findings

**(1) Confidence đã calibrate / cờ OOD / cờ "low-homology, đừng tin"**
- bindEmbed21 **có** một "reliability index" nhưng nó chỉ là **biến đổi đơn điệu của xác suất sigmoid**, không phải calibration: "RI ranging from 0 (unreliable; probability = 0.5) to 9 (very reliable; probability = 1.0)", công thức `RI(p) = (0.5−p)·9/0.5` nếu `p<0.5`, `(p−0.5)·9/0.5` nếu `p≥0.5` — [PMC8668950](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/) (đã kiểm). Không có reliability diagram, ECE, hay abstention.
- GPSite chỉ tổng hợp điểm residue thành điểm protein bằng cách lấy trung bình top-k, **không hề nói tới calibration hay OOD** — [PMC11023698](https://pmc.ncbi.nlm.nih.gov/articles/PMC11023698/) (đã kiểm)
- Tìm kiếm chuyên về "binding site predictor calibrated uncertainty out-of-distribution web server" **không trả về web server nào** tích hợp cả ba; các công trình về calibration/UQ chỉ nằm ở tầng method và ở ligand khác: temperature scaling cho protein–RNA binding site — [JCIM 65(12):6310](https://pubs.acs.org/jcisd8/article-abstract/65/12/6310/3687208/Uncertainty-Quantification-and-Temperature-Scaling); "CAP" calibrated abstention cho TCR–pMHC dưới epitope shift (PLM features + temperature scaling + conformal selective prediction) — [arXiv 2604.13254](https://arxiv.org/pdf/2604.13254); "RELIABLE-BA" cho binding affinity, cải thiện Expected Calibration Error — [arXiv 2607.17601](https://arxiv.org/pdf/2607.17601) (đã kiểm tiêu đề/snippet; chưa đọc toàn văn)
- NAR WSI 2025 chỉ yêu cầu **tài liệu hoá "capabilities and limitations"**, không yêu cầu calibration — [PMC12230694](https://pmc.ncbi.nlm.nih.gov/articles/PMC12230694/) (đã kiểm)

**(2) Hiển thị homolog gần nhất đã dùng để ra dự đoán**
- bindEmbed21HBI **chuyển annotation từ hit MMseqs2** ("two MMseqs2 iterations, at E-value ≤10⁻³"; "if this hit contained any binding annotations in the aligned region, annotations were transferred between aligned positions") nhưng bài báo **không nói là identifier của protein nguồn được báo cho người dùng** — [PMC8668950](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/) (đã kiểm; đây là **absence of evidence** trong chính bài báo của phương pháp)
- ATPbind là template-based (S-SITEatp/TM-SITEatp) nhưng trang server chỉ mô tả output là **binding site + pocket (PocHunter)**, không mô tả việc liệt kê template/homolog cho người dùng — [zhanggroup.org/ATPbind](https://zhanggroup.org/ATPbind/) (đã kiểm, scrape HTML)
- PrankWeb hiển thị **conservation** mapping lên structure, nhưng conservation là điểm tổng hợp từ MSA, **không phải danh sách homolog có thể bấm vào** — [NAR 50:W593](https://academic.oup.com/nar/article/50/W1/W593/6591527) (đã kiểm)

**(3) Giải thích ngôn ngữ tự nhiên / có dẫn nguồn văn liệu**
- **Không một predictor binding-site nào** trong danh sách trên có tầng giải thích NL (đã kiểm: không mục nào trong các bài/trang đã đọc đề cập)
- Ban biên tập NAR WSI 2025 **chủ động từ chối** các đề xuất kiểu chatbot: "The trend toward using large-language models (LLMs) has reached scientific web servers", nhưng các submission dạng chatbot bị "unreliable output or 'hallucinations'" và **"None ultimately met publication standards"** — [PMC12230694](https://pmc.ncbi.nlm.nih.gov/articles/PMC12230694/) (đã kiểm). **Đây là tín hiệu venue cực kỳ quan trọng cho đề tài: thêm LLM mà không grounding = lý do bị từ chối.**
- Xem KQ5 cho các hệ protein+LLM hiện có.

**(4) Reference database có phiên bản / cập nhật được mà không retrain**
- PrankWeb có **"prediction versioning tracking"** và DB tiền tính toán cho PDB, cộng với caching theo hash — [NAR 53:W466](https://academic.oup.com/nar/article/53/W1/W466/8136464) (đã kiểm). Nhưng đây là **versioning của kết quả dự đoán**, không phải reference DB có thể thay nóng.
- GPSiteDB là **snapshot tiền tính toàn Swiss-Prot**, không phải reference store cho inference — [PMC11023698](https://pmc.ncbi.nlm.nih.gov/articles/PMC11023698/) (đã kiểm)
- bindEmbed21HBI dùng MMseqs2 trên một DB annotation (BioLiP-dẫn xuất) nhưng bài báo mô tả nó như **thành phần cố định của pipeline**, không có mô tả cơ chế cập nhật DB cho người dùng cuối — [PMC8668950](https://pmc.ncbi.nlm.nih.gov/articles/PMC8668950/) (đã kiểm)

### Inferences

- **suy luận**: Bốn khoảng trống này **ghép đúng vào thiết kế kỹ thuật mà đề tài đã chốt** (frozen PLM + mCNN + k-NN retrieval trên embedding). k-NN retrieval cho sẵn, miễn phí, hai thứ không ai có: (a) **danh sách neighbor gần nhất** để hiển thị như "evidence panel", và (b) **khoảng cách tới neighbor gần nhất làm proxy OOD** để bật cờ "low-homology, do not trust". Nói cách khác, giá trị tool paper không nằm ở mCNN mà nằm ở việc **phơi bày retrieval ra UI**.
- **suy luận**: Vì reference store là **index k-NN tách rời weights**, việc "cập nhật DB mà không retrain" là tính năng **gần như miễn phí về kỹ thuật nhưng chưa ai bán**. Đáng đặt thành tính năng hạng nhất (reference DB có số phiên bản, ghi trong mỗi kết quả: "predicted with refDB v2026-03").
- **suy luận**: Vì PredictProtein sập và LambdaPP defunct, **bindEmbed21 hiện không có giao diện web nào cho người làm sinh học** → một web server sequence-only chạy được, dù mô hình tương đương, vẫn có giá trị sử dụng thật tại 10/2026.

### Gaps

- Không xác nhận được **bằng thực nghiệm trên UI** (mở trình duyệt, submit) rằng GPSite/ATPbind không hiển thị homolog — kết luận dựa trên bài báo và HTML tĩnh. GPSite là SPA nên scrape HTML không thấy nội dung. **Cần một lượt kiểm thủ công bằng trình duyệt trước khi viết câu "không ai làm X" vào đề cương.**
- Không tìm được bài nào đo "calibration của binding-site predictor trên protein low-homology" để dẫn làm động lực định lượng.

---

## KQ3. Venue và kỳ vọng cho một đóng góp dạng tool/application trong bioinformatics

### Takeaway

Bốn venue khả thi có yêu cầu rất khác nhau: NAR Web Server Issue là khó nhất (gatekeeping bằng one-page proposal trước 20/12, phải **cam kết bảo trì ≥5 năm**, HTTPS/443, không tracking cookie, phải có sample data + help page giải thích cách đọc kết quả); Bioinformatics Application Notes rẻ hơn (≤4 trang, bảo trì **2 năm**); JOSS yêu cầu kỷ luật engineering (OSI license, test tự động/CI, community guidelines, lịch sử commit nhiều tháng–năm) nhưng **không nhận bài trình bày kết quả nghiên cứu mới**.

### Cited Findings

**NAR Web Server Issue** — [Submitting to the Web Server Issue](https://academic.oup.com/nar/pages/submission_webserver) (đã kiểm, trích nguyên văn)
- Quy trình 2 bước: nộp **one-page summary** trước **20/12** tới `ds.narwbsrv@gmail.com`; summary phải có mô tả input data / output / processing method, PubMed ID của công bố method trước đó, 2–4 keyword, khai báo nếu là update, khai báo nếu là resubmission, tên + affiliation tác giả.
- Yêu cầu bắt buộc với application: "be of interest to a broad scientific audience", "be simple to use", "provide novelty or a clear benefit over similar applications", "be functional on the date of the proposal submission", "include a simple mechanism to **try out sample data provided by the authors**", "contain **help pages and/or a tutorial with links to sample output** in English", "include a standard licence that allows **free access for non-commercial use**".
- Help page phải "include information on **how to interpret the results** returned by the applications".
- **Loại trực tiếp** nếu: "require data preprocessing with other tools", "require installing further software", hoặc là "updates of applications that had been published within the last 2 years" (khoảng cách tối thiểu 2 năm để tái công bố).
- Kỹ thuật: "must use the **HTTPS protocol and run on the http standard port (443)**"; "provide a cookie consent form when permanent cookies are used — Third-party and tracking cookies must not be set by default"; "must not… use tracking and third-party cookies".
- Chất lượng: "The software must be **completely functional and have been extensively tested** at the time of submission."
- **Bảo trì**: "It is expected that web servers and web services will be **maintained for at least five years**."
- Độ dài: "should typically be **4–5 printed journal pages**". Deadline bản thảo: "2 months after the date of the approval email".
- Editorial 2025: nhận **72 web server**; phải chạy **không bắt buộc login** (trừ dữ liệu y tế nhạy cảm), **free và open-access**, không đòi thanh toán/thẻ tín dụng; cần "comprehensive documentation of capabilities and limitations", phải dùng được bởi **người không phải bioinformatician** (tránh bắt buộc command line), output cần "contextual output features like gene annotations, external links, and filtering options"; **mọi đề xuất kiểu LLM chatbot đều bị từ chối vì hallucination** — [PMC12230694](https://pmc.ncbi.nlm.nih.gov/articles/PMC12230694/) (đã kiểm)

**Bioinformatics (OUP) — Application Notes** — [Author guidelines](https://academic.oup.com/bioinformatics/pages/author-guidelines) (đã kiểm, trích nguyên văn)
- Độ dài: "**Up to 4 pages; this is approx. 2,600 words or 2,000 words plus one figure**"
- "Software or data must be **freely available to non-commercial users**"; "Availability and Implementation must be clearly stated in the article"
- **Bảo trì**: tác giả phải "ensure that the software is **available for a full two years following publication**"
- Tài liệu: "detailed documentation on how to acquire, install, and run the software" bao gồm "information on the **purpose and values of all optional parameters**"
- Source: "freely available at **stable URLs (e.g. github, bitbucket) without request** to non-commercial users"
- Tái lập: phải có "appropriate **test data**" và "information on **how to reproduce results/figures** described in the manuscript"; data availability statement là **bắt buộc**; khuyến khích open source license, ngôn ngữ lập trình **non-proprietary**, và submit lên Code Ocean.

**JOSS** — [Review criteria](https://joss.readthedocs.io/en/latest/review_criteria.html), [Submitting a paper](https://joss.readthedocs.io/en/latest/submitting.html), [Review checklist](https://joss.readthedocs.io/en/latest/review_checklist.html) (đã kiểm)
- Software phải **open source theo định nghĩa OSI**, host nơi browse source được **không cần phê duyệt**, có "obvious research application", và tác giả nộp phải là major contributor.
- **Substantial scholarly effort**: cần "sustained development over time (preferably **months or years**)"; "**all or most commits concentrated in the last few weeks before submission**" bị đánh dấu là không chấp nhận và reviewer phải báo editor ngay.
- Documentation phải có: statement of need, installation instructions (tự động xử lý dependency), example usage, **API documentation**, community guidelines cho "contribute to the software, report issues or problems with the software, seek support". "API is undocumented" = không đạt.
- Functionality: reviewer **phải tự cài và verify core functionality**; cần **automated test suite + CI**, hoặc documented manual verification steps; "no way for you, the reviewer, to objectively assess whether the software works" = không đạt.
- Paper: **750–1750 từ**; "**must not focus on new research results** accomplished with the software"; paper.md + .bib phải nằm trong repo git cùng software.
- Loại trừ: "minor 'utility' packages, including 'thin' API clients, are not acceptable"; phải feature-complete, "no half-baked solutions".

### Inferences

- **suy luận**: Với một luận văn, **Bioinformatics Application Note là mục tiêu thực tế nhất** (4 trang, bảo trì 2 năm), còn NAR WSI là "stretch goal" vì đòi cam kết 5 năm — điều một sinh viên tốt nghiệp rất khó hứa. JOSS thì **không phù hợp làm venue chính** cho một luận văn có đóng góp method, vì JOSS cấm bài trình bày kết quả nghiên cứu mới; nhưng JOSS **rất phù hợp làm venue thứ hai** cho phần package/CLI.
- **suy luận**: Danh sách yêu cầu NAR gần như là một **checklist thiết kế sản phẩm có thể dùng trực tiếp làm acceptance criteria của đề tài**: sample data bấm-một-nút, help page nói cách đọc kết quả, không bắt install gì thêm, HTTPS/443, không tracking cookie, license free cho non-commercial, không đòi login. Nên copy thẳng vào mục "yêu cầu phi chức năng" của đề cương.
- **suy luận**: Việc NAR 2025 từ chối toàn bộ submission LLM-chatbot nghĩa là nếu đề tài làm tầng giải thích LLM, **phải trình bày nó như "retrieval-grounded, citation-backed, có đánh giá faithfulness"**, không phải "chatbot". Nếu không có số đo về grounding, tính năng này là **liability khi review**, không phải điểm cộng.

### Gaps

- **BMC Bioinformatics "Software" article guidelines**: tôi **không kiểm được** (không nằm trong các truy vấn đã chạy). Cần tra riêng `biomedcentral.com/bmcbioinformatics/submission-guidelines`.
- Không tìm được thống kê **tỷ lệ chấp nhận (acceptance rate)** của NAR WSI; editorial 2025 công bố 72 server được nhận nhưng "doesn't specify total submission numbers" — [PMC12230694](https://pmc.ncbi.nlm.nih.gov/articles/PMC12230694/).
- Không kiểm được liệu NAR WSI có yêu cầu riêng về **tool dùng LLM** (vd. khai báo prompt, nhiệt độ, phiên bản model) hay chỉ từ chối ad hoc.

---

## KQ4. Kiến trúc tham chiếu de facto + văn liệu về tuổi thọ / link rot

### Takeaway

**PrankWeb (3 và 4) là kiến trúc tham chiếu tốt nhất và được tài liệu hoá rõ nhất trong niche này**: tách UI / storage / execution, mỗi task một Docker image qua docker-compose, hàng đợi **Celery**, caching theo **hash của (structure, pocket, params)**, REST API v2, **>800.000 protein tiền tính toán**, viewer **Mol\*** + **RCSB Saguaro 1D feature viewer**, export JSON/CSV/PDBQT/ChimeraX, CC BY 4.0. Về tuổi thọ, con số đáng trích nhất: trong 133 ngày theo dõi 2.396 công cụ, **chỉ 31% luôn hoạt động, 48,4% thỉnh thoảng, 20,6% chưa bao giờ**; availability giảm gần như tuyến tính theo tuổi (~90% cho tool 2019–2020 so với **~50% cho tool 2010**).

### Cited Findings

**PrankWeb 3 (NAR 2022, 50:W1:W593)** — [academic.oup.com/nar/article/50/W1/W593](https://academic.oup.com/nar/article/50/W1/W593/6591527) (đã kiểm, trích nguyên văn)
- "The new modular architecture **strictly separates web-based user interface, data storage, and an execution component**"
- "**Each component corresponds to a Docker image.** Combined with **docker-compose**, it is easy to deploy and update PrankWeb instances." Người dùng có thể deploy **chỉ execution component** để xử lý dữ liệu riêng tư mà không gửi cho bên thứ ba.
- Input: PDB ID, UniProt accession (lấy model từ AlphaFold DB), file upload; hỗ trợ cả **PDB và mmCIF**.
- **Tiền tính toán >800.000 protein** (AlphaFold DB model organisms + Swiss-Prot) → trả kết quả tức thì không phải tính.
- **REST API v2**: POST để tạo prediction mới, GET để lấy status, log, structure, và archive kết quả.
- Output: binding site map lên structure, nhiều chế độ hiển thị (surface, cartoon, balls-and-sticks); tải archive gồm **PyMOL visualization, parameters, logs, pocket data dạng CSV**.
- Source: https://github.com/cusbg/p2rank-framework

**PrankWeb 4 (NAR 2025, 53:W1:W466, 07/07/2025)** — [academic.oup.com/nar/article/53/W1/W466](https://academic.oup.com/nar/article/53/W1/W466/8136464) (đã kiểm, trích nguyên văn)
- **Hệ module hai tầng**: client-side module (task nhẹ chạy trong browser, vd. tính thể tích pocket) và server-side module ("computationally intensive and demands substantial resources" như docking), server-side dùng "**Celery job queues**" với "**each server-side task encapsulated within a dedicated Docker image**, which is integrated into the architecture using **Docker Compose**".
- Mỗi module có thể gắn một **visualization module** tác động lên kết quả của nó.
- Stack cụ thể: chuyển từ **LiteMol sang Mol\*** cho viewer 3D; **RCSB Saguaro 1D Feature Viewer** cho trục sequence; **AutoDock Vina** để docking; **OpenBabel** (SMILES→3D) và **MGLTools** (chuẩn bị receptor/ligand).
- **Caching**: "a caching mechanism that assigns a **unique hash to each task**" dựa trên structure, pocket và parameters. "**Task history for individual users is stored in the browser**, allowing easy access to the previously computed results."
- Có **prediction versioning tracking**; DB PDB tiền tính toán mới; P2Rank 2.5 nhanh gấp ~2 lần.
- Export: **JSON, PDBQT, ChimeraX visualization scripts**. Source: GitHub `p2rank-framework` + **Zenodo DOI 10.5281/zenodo.15319389 và 10.5281/zenodo.15303370**. License: **CC BY 4.0**.
- Phụ trợ đã kiểm: `docker-compose-prankweb.yml` trong repo cho thấy dùng **RabbitMQ làm message broker** — [cusbg/prankweb](https://github.com/cusbg/prankweb/blob/main/docker-compose-prankweb.yml) (đã kiểm sự tồn tại của file qua search result; **chưa đọc nội dung file**)

**Kiến trúc "rẻ" 2025: Seq2Bind** — host trên **Render** (PaaS free/hobby tier), phát hành source + weight qua **Google Colab notebook** thay vì repo chuẩn — [PMC12639246](https://pmc.ncbi.nlm.nih.gov/articles/PMC12639246/) (đã kiểm). Đây là **bằng chứng rằng NAR Genomics and Bioinformatics vẫn nhận tool paper với hạ tầng cực nhẹ**.

**Văn liệu về tuổi thọ / link rot (số liệu để trích)**

*Kern, Fehlmann, Keller, "On the lifetime of bioinformatics web services", NAR 2020;48(22):12523* — [academic.oup.com/nar/article/48/22/12523](https://academic.oup.com/nar/article/48/22/12523/6018434) (đã kiểm, toàn văn qua fetch)
- Cỡ mẫu: **2.396 công cụ bioinformatics duy nhất** từ **2.727 bài báo** sau 2010; tải **318.668 index file** trong kỳ theo dõi.
- Trong **133 ngày**: **31% luôn hoạt động, 48,4% thỉnh thoảng, 20,6% chưa bao giờ**; **74,3% truy cập được vào ngày đầu (13/04/2020)**.
- Availability theo năm công bố: **~90% cho tool 2019–2020**, **~50% cho tool 2010**; "almost linear decreasing availability" qua một thập kỷ.
- Downtime: **median downtime liên tiếp 1 ngày, mean 2,9 ngày**, thường dưới 5 ngày.
- **Thí nghiệm "rescue"**: với 47 tool mới (2019–2020) ban đầu không truy cập được — **57,4% tác giả liên hệ có phản hồi; 51,1% tool phục hồi được; 29,8% hoạt động lại trong vòng 1 ngày sau khi liên hệ**. (→ nhiều outage chỉ là vận hành, không phải mất hẳn.)
- Hosting: **71,6% host tại viện nghiên cứu, 13,8% trên cloud**; **40,5% được index trong bio.tools**.
- Citation: tool từng truy cập được có citation cao hơn đáng kể so với tool không bao giờ truy cập được (p từ **1,278×10⁻⁷ đến 6,758×10⁻¹⁵**).
- **Khuyến nghị cho developer** (4 nhóm): bảo mật — "**Switch to production mode when deploying**" + cập nhật bảo mật định kỳ; tái lập — "**Use virtual machines or container virtualization (e.g. Docker)**" + version control; bảo trì — giảm công sức migration, **tài liệu hoá quy trình reset**; khả dụng — "**Provide access over a domain name instead of an IP address**" + tutorial chi tiết.
- Dẫn lại nghiên cứu trước: **72% web server NAR 2003–2009 vẫn ở địa chỉ gốc**.

*Schultheiss et al., "Persistence and Availability of Web Services in Computational Biology", PLoS ONE 2011* — [journals.plos.org](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0024914), [PMC3178567](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3178567/) (đã kiểm qua snippet search)
- Trong 927 web server NAR 2003–2009: **72% còn ở địa chỉ gốc, 9% đã offline**; khoảng **27% URL đã mục** từ lúc công bố.
- **"For 24% of services, there is no plan for maintenance."**
- ⚠️ *Lưu ý nguồn*: các con số này tôi lấy từ **tổng hợp của search engine + dẫn lại trong bài NAR 2020**, chưa đọc toàn văn PLoS ONE. Cần xác minh lại trước khi trích vào đề cương.

*Survey cũ hơn, Genomics Proteomics Bioinformatics 2007, "A Survey of the Availability of Primary Bioinformatics Web Resources"* — [PMC5054106](https://pmc.ncbi.nlm.nih.gov/articles/PMC5054106/), [PDF](https://academic.oup.com/gpb/article-pdf/5/1/70/57483040/gpb_5_1_70.pdf), [PubMed 17572367](https://pubmed.ncbi.nlm.nih.gov/17572367)
- **80% URL khả dụng 100% thời gian**; **91% khả dụng cao (up ≥90% thời gian)**; **chỉ 4% có accessibility thấp (<50%)**.
- ⚠️ Con số lạc quan này **mâu thuẫn rõ** với Kern 2020 (31% luôn hoạt động). Lý do khả dĩ: survey 2007 chỉ xét **primary resources** (database lớn, được tài trợ dài hạn) trong **cửa sổ thời gian ngắn**, còn Kern 2020 xét **mọi tool** trong 133 ngày và theo tuổi công bố. **Nên trích cả hai và nêu rõ sự khác biệt về đối tượng**, đừng chọn im lặng một bên.

*Link decay liên ngành* — [BMC Bioinformatics 14(S14):S5, "A cross disciplinary study of link decay and the effectiveness of mitigation techniques"](https://link.springer.com/article/10.1186/1471-2105-14-S14-S5) (đã kiểm tiêu đề; **chưa đọc toàn văn/chưa có số**)

### Inferences

- **suy luận**: Kiến trúc nên imitate cho đề tài ATP = **"PrankWeb-lite"**: (1) tách 3 tầng UI / storage / execution; (2) một Docker image cho execution để người dùng tự chạy nội bộ (giải quyết luôn vấn đề dữ liệu riêng tư và vấn đề "server sập sau khi tốt nghiệp"); (3) hàng đợi (Celery+Redis hoặc RQ; RabbitMQ nếu muốn giống PrankWeb) **thay vì request đồng bộ**, vì PLM inference tốn giây-đến-phút; (4) **cache theo hash của (sequence, model version, refDB version)** — với inference sequence-only thì hash chính là SHA của chuỗi, rẻ hơn PrankWeb nhiều; (5) **URL kết quả bền** `/result/<hash>` thay cho email như ATPbind; (6) viewer **Saguaro 1D feature viewer** cho track per-residue (đúng bài toán per-residue, nhẹ hơn Mol*), tuỳ chọn Mol* nếu có structure dự đoán.
- **suy luận**: Vì đề tài là **sequence-only + frozen PLM + k-NN**, một tập **tiền tính toàn bộ RTK người** (quy mô vài trăm–vài nghìn protein, nhỏ hơn 800k của PrankWeb nhiều) là hoàn toàn khả thi, và đó chính là tính năng "instant result" mà NAR WSI đánh giá cao (và cũng là sample data bấm-một-nút mà họ bắt buộc).
- **suy luận**: Khuyến nghị "domain name instead of IP" và "Docker" của Kern 2020 giải thích chính xác vì sao PUResNet (`bioinfo.konkuk.ac.kr:8443` → 404) và ScanNet (`scanneteam.com` → DNS fail) chết trong khi P2Rank sống. **Đây là bằng chứng để biện minh cho quyết định kiến trúc trong đề cương**, không phải chỉ lời khuyên chung.
- **suy luận**: Rate limiting không được bàn tới trong bất kỳ bài nào tôi đọc → **không có chuẩn công bố**; nên tự đặt (vd. N job/IP/giờ) và nói rõ trong help page, vì NAR yêu cầu không login nên rate limit theo IP là cơ chế duy nhất chống lạm dụng.

### Gaps

- **Không tìm được bài "lessons learned" chuyên về vận hành web server bioinformatics** (kiểu post-mortem). Những gì có là phần khuyến nghị trong Kern 2020 và editorial NAR.
- Không có số liệu công bố về **traffic/số job** của PrankWeb hay GPSite → không biết quy mô tải thực tế cần thiết kế cho.
- Không kiểm được nội dung thực tế của `docker-compose-prankweb.yml` (chỉ thấy tên file và mention RabbitMQ qua search) → **danh sách service chính xác chưa xác nhận**.
- Chưa tìm được tài liệu nào bàn **SLURM backend** cho loại web server này (giả thuyết: các nhóm lớn dùng, nhưng không viết ra).

---

## KQ5. Có công cụ nào trong niche này ghép predictor với tầng giải thích LLM có dẫn nguồn?

### Takeaway

**Không.** Tôi không tìm được bất kỳ công cụ đã công bố nào ghép một predictor binding-site với tầng giải thích LLM có citation. Các hệ protein+LLM hiện có (Prot2Text/V2, ProtChatGPT, ProteinGPT, Prot2Chat) sinh **mô tả chức năng ở mức protein, free-text, không retrieval-grounded, không citation**; còn các agent bioinformatics (BioMANIA, Biomni) là **orchestrator chạy tool/API**, không phải tầng giải thích cho dự đoán per-residue. Khoảng trống này vừa được một bài 2026 nêu thành tiêu chí đánh giá ("Evidence" axis) và kết luận là **các agent hiện tại thất bại ở đó**.

### Cited Findings

**Protein → text (mức protein, không citation)**
- **Prot2Text**: kết hợp GNN + LLM để "predict protein functions in free-text form", sinh "detailed and accurate descriptions of proteins' functions in free text", tích hợp cả structural và sequential information — [arXiv 2307.14367](https://arxiv.org/abs/2307.14367) (đã kiểm qua abstract/snippet)
- **Prot2Text-V2**: sequence-to-text multimodal, encoder **ESM-3B** + decoder **LLaMA-3.1-8B-Instruct** qua một "lightweight nonlinear modality projector", đóng góp chính là "Hybrid Sequence-level Contrastive Alignment Learning (H-SCALE)"; sinh mô tả chức năng free-form **trực tiếp từ sequence** — [arXiv 2505.11194](https://arxiv.org/pdf/2505.11194), [NeurIPS 2025](https://mlanthology.org/neurips/2025/fei2025neurips-prot2textv2/) (đã kiểm snippet)
- **Prot2Chat**: "protein large language model with early fusion of text, sequence, and structure", **Bioinformatics 41(8):btaf396** (2025) — [academic.oup.com/bioinformatics/article/41/8/btaf396](https://academic.oup.com/bioinformatics/article/41/8/btaf396/8215464) (đã kiểm tiêu đề + venue; **chưa đọc toàn văn**). Đáng chú ý: **đây là bằng chứng Bioinformatics có nhận bài protein-LLM**, trái với việc NAR WSI từ chối chatbot.
- **ProteinGPT / ProtChatGPT**: align không gian sequence (và structure) với không gian text sinh-y để "generate functional descriptions"; ProtChatGPT dùng hai module riêng encode sequence và structure rồi align với natural language (đã kiểm qua tổng hợp search; **chưa đọc bài gốc** → nhãn yếu hơn)
- ⚠️ **Không bài nào trong số trên có citation/retrieval grounding**: đặc điểm chung là sinh text từ representation học được, **không có bước retrieve document** (đã kiểm: không mô tả nào trong các abstract/snippet đã đọc đề cập retrieval hay citation).

**Agent bioinformatics**
- **BioMANIA** ("BioinforMatics dAta aNalysIs through conversAtion"): pipeline hiểu chỉ thị ngôn ngữ tự nhiên rồi "interpreting the user's intent, breaking it down into specific tasks…, mapping tasks to API calls, executing the APIs with inferred arguments, and troubleshooting any coding errors"; học API từ **source code và documentation** của các package Python open-source; phân tích **12 tool** và rút ra **11 vấn đề thường gặp** thành guideline để thiết kế tool "ChatBot-compatible"; ứng dụng minh hoạ là single-cell gene expression — [bioRxiv 2023.10.29.564479](https://www.biorxiv.org/content/10.1101/2023.10.29.564479.full.pdf) (đã kiểm snippet). **Đây là loại "giao diện hội thoại cho tool", không phải tầng giải thích cho dự đoán.**
  - *Điểm đáng dùng cho đề tài*: danh sách "11 common issues" + guideline "ChatBot-compatible tool design" là tài liệu trực tiếp hữu ích nếu đề tài muốn API dễ cho agent gọi. **Chưa đọc được danh sách 11 mục** → gap.
- **Biomni** (Stanford): "A General-Purpose Biomedical AI Agent" — [biomni.stanford.edu/paper.pdf](https://biomni.stanford.edu/paper.pdf) (đã kiểm tồn tại; chưa đọc)
- Survey: "The rise and potential opportunities of large language model agents in bioinformatics and biomedicine" — [PMC12602188](https://pmc.ncbi.nlm.nih.gov/articles/PMC12602188/) (đã kiểm tồn tại; chưa đọc)

**Tiêu chí "Evidence" cho agentic bio tools (bài 2026, rất đúng chủ đề)**
- Pham & Hy, **"Evaluating Agentic Bioinformatics through Function, Evidence, and Validation"**, arXiv 2607.27556v1, **07/2026**: đề xuất framework 3 trục; trục **Evidence** yêu cầu "agent outputs be grounded in verifiable sources", output "should include **citations or references to retrieved documents**, establishing **traceability** between claims and their source material"; trục **Validation** xét tính đúng + robustness của cơ chế kiểm chứng. **Phát hiện chính: "many existing bioinformatics agents fail to consistently provide proper evidence grounding… tools frequently generate outputs without adequate citation of source documents or retrieved evidence, undermining reproducibility"** — [arXiv 2607.27556](https://arxiv.org/pdf/2607.27556) (đã kiểm, fetch PDF)
- **RAGulate**: framework cho "post-hoc, **literature-grounded verification** through a retrieval-augmented generation strategy where an LLM is augmented with a literature retrieval step through an external domain-specific knowledge database" (đã kiểm qua snippet search; **chưa tìm được bài gốc/URL chính thức** → gap). Nếu xác minh được, đây là **mẫu hình gần nhất** với "tầng giải thích có dẫn nguồn" mà đề tài muốn.
- Grounding/citation nói chung: **ReClaim** sinh reference và answer xen kẽ, cho citation **mức câu**, đạt citation accuracy **90%**, NAACL 2025 Findings — [arXiv 2407.01796](https://arxiv.org/abs/2407.01796); **CiteGuard** validate citation attribution bằng retrieval — [arXiv 2510.17853](https://arxiv.org/pdf/2510.17853); **MEGA-RAG** multi-evidence guided answer refinement để giảm hallucination trong y tế công — [PMC12540348](https://pmc.ncbi.nlm.nih.gov/articles/PMC12540348/) (đã kiểm snippet). Đây là nguồn để **mượn metric đánh giá grounding**, không phải tool protein.

### Inferences

- **suy luận**: Có một **mâu thuẫn venue cần xử lý rõ trong đề cương**: NAR WSI 2025 từ chối mọi server kiểu LLM chatbot vì hallucination ([PMC12230694](https://pmc.ncbi.nlm.nih.gov/articles/PMC12230694/)), trong khi Bioinformatics vẫn xuất bản protein-LLM (Prot2Chat, btaf396). → Nếu đề tài muốn NAR WSI, tầng LLM phải là **tính năng phụ, tắt được, có citation bắt buộc và có số đo faithfulness**; nếu muốn an toàn hơn, nhắm Bioinformatics.
- **suy luận**: Khoảng trống chính xác và có thể bảo vệ được là: **"giải thích per-residue, được grounding bằng retrieval, trong một predictor binding-site"**. Prot2Text giải thích **cả protein**, không giải thích **một residue**; BioMANIA điều phối **tool**, không giải thích **dự đoán**. Không ai làm per-residue + grounded.
- **suy luận**: Cấu trúc grounding rẻ nhất và dễ bảo vệ nhất cho đề tài **không cần văn liệu**: grounding vào **neighbor k-NN có annotation BioLiP/UniProt** ("residue K721 được dự đoán là ATP-binding; 7/10 neighbor gần nhất trong embedding space là residue ATP-binding đã xác nhận thực nghiệm, gần nhất là EGFR K745, cosine 0,94"). Đây là citation tới **record cơ sở dữ liệu**, verify được tự động, không hallucinate được — khác hẳn với citation văn liệu do LLM sinh. Nên dùng cái này làm tầng 1, và LLM chỉ **diễn đạt lại** evidence đã retrieve (templated/constrained generation), không được thêm fact mới.

### Gaps

- **Không xác minh được RAGulate** (không tìm thấy bài gốc) — nhưng đây là nguồn tiềm năng quan trọng nhất cho ý "literature-grounded verification". Nên tra lại.
- **Chưa đọc toàn văn** Prot2Chat, ProteinGPT, ProtChatGPT → không chắc chắn 100% là chúng **không có** retrieval. Kết luận "không có citation" dựa trên abstract/mô tả. **Cần đọc kỹ trước khi viết "chưa ai làm" vào luận văn.**
- Không tìm được bất kỳ **benchmark về chất lượng giải thích per-residue trong protein** (kiểu "explanation faithfulness cho binding-site prediction") → nếu đề tài làm tính năng này, **phải tự thiết kế cách đánh giá**, đây là rủi ro lớn nhất về mặt reviewable.
- Chưa đọc được danh sách **"11 common issues"** của BioMANIA (guideline thiết kế tool thân thiện chatbot) — hữu ích cho thiết kế API nếu lấy được.
