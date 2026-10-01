# Khả thi kỹ thuật và reference stack để triển khai web tool RAG hai lớp cho tin sinh, ngân sách gần bằng 0, không có GPU cục bộ

> **Ngày đọc nguồn: 01/10/2026.** Mọi mức giá và hạn mức free-tier đều được đọc trong ngày này; các trang này thay đổi thường xuyên, phải kiểm lại trước khi đưa số vào đề cương bảo vệ.
>
> **Quy ước ghi nhãn trong ghi chú này:**
> - **đã kiểm** = số trích trực tiếp từ nguồn, có link.
> - **suy luận** = phép tính của tôi, có viết rõ công thức; **không phải số đo**.
> - **chưa kiểm** = tôi không tìm được nguồn trong phiên này → nằm ở mục Gaps.

---

## 1. Chi phí inference của PLM: RAM/VRAM và độ trễ CPU

### Takeaway

ProtT5-XL-U50 **không phù hợp để chạy đồng bộ trên CPU free-tier**: bản fp16 encoder-only được chính model card nói là "fully usable on 8 GB of video RAM" nhưng **half precision không chạy được trên CPU** — phải cast về `float()`, tức quay lại footprint fp32. Các lựa chọn nhỏ hơn (ESM-2 150M/35M/8M, ESM-C 300M) có footprint cỡ vài trăm MB và là đường thoát thực tế duy nhất nếu muốn CPU-only. Đáng lưu ý: free tier của HuggingFace Spaces là **2 vCPU / 16 GB RAM**, chứ không phải 512 MB–2 GB như giả định ban đầu của đề bài — nên "không giữ nổi mô hình nhiều GB" **không còn là giới hạn về RAM**, mà là giới hạn về **độ trễ CPU** và về **chính sách host** (xem mục 2).

### Cited Findings

**ProtT5-XL-U50 (Rostlab/ProtTrans)**
- Model card bản encoder-only half precision: "only contains the encoder portion of the original ProtT5-XL-UniRef50 model using half precision (float16)" và model dựa trên kiến trúc `t5-3b` — [Rostlab/prot_t5_xl_half_uniref50-enc](https://huggingface.co/Rostlab/prot_t5_xl_half_uniref50-enc) (**đã kiểm**)
- Cảnh báo CPU, trích nguyên văn: "Currently (06/2022) half-precision models cannot be used on CPU. If you want to use the encoder only version on CPU, you need to cast it to its full-precision version (`model=model.float()`)." — [cùng nguồn](https://huggingface.co/Rostlab/prot_t5_xl_half_uniref50-enc) (**đã kiểm**)
- Phải set dtype tường minh, nếu không embedding sẽ ra full precision: "Please make sure to explicitly set the model to `float16` (`T5EncoderModel.from_pretrained('Rostlab/prot_t5_xl_half_uniref50-enc', torch_dtype=torch.float16)`) otherwise, the generated embeddings will be full precision." — [cùng nguồn](https://huggingface.co/Rostlab/prot_t5_xl_half_uniref50-enc) (**đã kiểm**)
- Yêu cầu VRAM: "This model is fully usable on 8 GB of video RAM" — [cùng nguồn](https://huggingface.co/Rostlab/prot_t5_xl_half_uniref50-enc) (**đã kiểm**)
- Chất lượng không mất khi dùng fp16: "these embeddings produced the same performance" trên nhiều downstream task — [cùng nguồn](https://huggingface.co/Rostlab/prot_t5_xl_half_uniref50-enc) (**đã kiểm**)

**Độ trễ GPU đã công bố (dùng làm mốc trên, KHÔNG phải số CPU)**
- ProtT5-XL: trung bình **0,12 s/protein người**, toàn bộ human proteome trong ~40 phút; với Nvidia Quadro RTX 8000, half precision, batch size 32 thì **0,025 s/protein** — [ProtTrans, arXiv:2007.06225](https://arxiv.org/pdf/2007.06225) (**đã kiểm**, qua tổng hợp kết quả tìm kiếm trên bài ProtTrans)
- ProstT5 encoder (cùng nhà Rostlab, cùng cỡ): human proteome ~35 phút, tức **~0,1 s/protein** với batch + fp16 trên 1× RTX A6000 48 GB — [Rostlab/ProstT5](https://huggingface.co/Rostlab/ProstT5) (**đã kiểm**)
- Bộ nhớ khi benchmark embedding: "ProtT5 is the most memory demanding model with 5176 ± 45 MB average and 15,763 ± 2 MB peak memory" — [Survey of Protein Sequence Embedding Models, PMC9963412](https://pmc.ncbi.nlm.nih.gov/articles/PMC9963412/) (**đã kiểm**)
- ANKH: "Ankh runs 2–11x faster for inference and requires only one GPU versus four for ProtT5's larger variants" — [cùng nguồn khảo sát](https://pmc.ncbi.nlm.nih.gov/articles/PMC9963412/) (**đã kiểm**)

**Kích thước các lựa chọn nhỏ hơn**
- ESM-2 650M: 650M tham số, 33 layer, 20 attention head, **hidden dim 1280** — [NVIDIA BioNeMo ESM-2 docs](https://docs.nvidia.com/bionemo-framework/2.1/models/esm2/) (**đã kiểm**)
- ESM-2 3B: 2,8B tham số, 36 layer, dim 2560; ESM-2 15B: 15B tham số, 48 layer, dim 5120 — [cùng nguồn](https://docs.nvidia.com/bionemo-framework/2.1/models/esm2/) (**đã kiểm**)
- ESM-C 300M: 300M tham số, 30 layer, **embedding dim 960**, 15 head — [MultiMolecule ESMC](https://multimolecule.danling.org/models/esmc/), [EvolutionaryScale blog: ESM Cambrian](https://www.evolutionaryscale.ai/blog/esm-cambrian) (**đã kiểm**)
- ESM-C 600M: 600M tham số, 36 layer, **embedding dim 1152**, 18 head — [cùng nguồn](https://multimolecule.danling.org/models/esmc/) (**đã kiểm**)

### Inferences

**Footprint trọng số = số tham số × số byte/tham số** (fp32 = 4 B, fp16 = 2 B, int8 = 1 B). Bảng dưới là **suy luận**, phép tính viết thẳng trong ô:

| Mô hình | Tham số | Dim | fp32 (×4 B) | fp16 (×2 B) | int8 (×1 B) |
|---|---|---|---|---|---|
| ProtT5-XL-U50 (full enc+dec) | ~3,0B | 1024 | 3e9×4 = **12,0 GB** | 3e9×2 = **6,0 GB** | **3,0 GB** |
| ProtT5-XL-U50 **encoder-only** | ~1,2B (chưa kiểm, xem Gaps) | 1024 | 1,2e9×4 = **4,8 GB** | 1,2e9×2 = **2,4 GB** | **1,2 GB** |
| ESM-2 650M | 650M | 1280 | **2,60 GB** | **1,30 GB** | **0,65 GB** |
| ESM-2 150M | 150M | chưa kiểm | **0,60 GB** | **0,30 GB** | **0,15 GB** |
| ESM-2 35M | 35M | chưa kiểm | **0,14 GB** | **0,07 GB** | **0,035 GB** |
| ESM-2 8M | 8M | chưa kiểm | **0,032 GB** | **0,016 GB** | **0,008 GB** |
| ESM-C 300M | 300M | 960 | **1,20 GB** | **0,60 GB** | **0,30 GB** |
| ESM-C 600M | 600M | 1152 | **2,40 GB** | **1,20 GB** | **0,60 GB** |

- **suy luận:** số 5176 MB average / 15 763 MB peak của ProtT5 trong bài khảo sát **lớn hơn nhiều** footprint trọng số thuần (4,8–12 GB phụ thuộc biến thể) — phần chênh là activation của self-attention, vốn tăng theo O(L²) với độ dài chuỗi L. Với thiết kế per-residue + cửa sổ đa quy mô, **activation chứ không phải trọng số** là thứ quyết định peak RAM khi gặp một chuỗi dài 2000+ residue. Phải đặt hard cap độ dài chuỗi (xem mục 3).
- **suy luận về độ trễ CPU:** chưa có số đo CPU nào công bố cho ProtT5 (xem Gaps). Nếu lấy mốc GPU 0,1 s/protein và giả định tỉ lệ CPU/GPU cho transformer inference nằm trong khoảng 30–100× (khoảng này **chưa kiểm**, chỉ là biên độ tôi dùng để khung hóa rủi ro), thì một protein 300 residue trên CPU sẽ mất **3–10 s**. Đây là con số *không được đưa vào đề cương như số đo* — phải tự benchmark trên chính WSL2 rồi ghi lại (xem "Việc cần làm" cuối file).
- **suy luận:** nếu free tier là 2 vCPU / 16 GB (xem mục 2), thì **mọi** mô hình trong bảng trên, kể cả ProtT5 encoder fp32 4,8 GB, đều *nạp được vào RAM*. Rào cản không phải RAM mà là (a) thời gian cold start tải 4,8 GB trọng số, (b) giây CPU mỗi request, (c) chính sách host.
- **suy luận:** với host RAM 512 MB – 2 GB (Render free, Cloud Run mặc định 512 MiB) thì ngưỡng chia là rõ: giữ được ESM-2 8M/35M/150M và (sát ngưỡng 2 GB) ESM-C 300M fp32 1,2 GB; **không** giữ được ESM-2 650M fp32 2,6 GB hay bất kỳ biến thể ProtT5 nào. Lưu ý footprint runtime còn phải cộng PyTorch + numpy + FAISS index (~0,3–0,8 GB tùy build, **chưa kiểm**).

### Gaps

- **Không tìm được bất kỳ số đo độ trễ CPU công bố nào** cho ProtT5-XL, ESM-2, ESM-C hay DistilProtBert. Mọi nguồn benchmark đều báo GPU. Đây là khoảng trống đo lường mà sinh viên **phải tự lấp** bằng benchmark riêng — và chính nó là một đóng góp nhỏ nhưng kiểm chứng được cho luận văn.
- Số tham số chính xác của **phần encoder** ProtT5-XL-U50: model card chỉ nói "based on t5-3b", không công bố param count của encoder. Con số ~1,2B trong bảng là ước lượng của tôi theo tỉ lệ encoder/decoder của T5, **chưa kiểm**.
- Embedding dim của ESM-2 8M / 35M / 150M: chưa đọc được model card từng bản trong phiên này (tên bản `esm2_t6_8M_UR50D`, `esm2_t12_35M_UR50D`, `esm2_t30_150M_UR50D` gợi ý layer count 6/12/30 nhưng dim thì cần đọc trực tiếp `config.json`).
- **DistilProtBert**: không tìm được param count, dim, hay số đo nào trong phiên này.
- **ANKH**: chỉ có mệnh đề so sánh tương đối ("2–11× faster"), không có param count/dim tuyệt đối.
- Không tìm được tài liệu nào xác nhận ProtT5/ESM-2 **chạy int8 trên CPU** cho kết quả embedding tương đương; không nên giả định.

---

## 2. Host ở đâu, free hoặc gần-free, tình hình tháng 10/2026

### Takeaway

Phát hiện quan trọng và **đổi cục diện**: HuggingFace Spaces đã **siết free tier** — Gradio và Docker Spaces nay **yêu cầu gói trả phí (PRO)** để tạo; tài khoản cá nhân free chỉ còn host được **tối đa 2 ZeroGPU Space (chỉ Gradio SDK)**, trong khi Static Spaces vẫn free cho mọi người. Nghĩa là cấu trúc free khả thi nhất không còn là "một container CPU free chạy mãi" mà là: **frontend static + backend dùng ZeroGPU theo quota ngày, hoặc serverless trả theo giây (Modal) nằm trong credit miễn phí $30/tháng**.

### Cited Findings

**HuggingFace Spaces** — [spaces-overview](https://huggingface.co/docs/hub/spaces-overview), [pricing](https://huggingface.co/pricing) (đọc 01/10/2026)
- Phần cứng mặc định: "Each Spaces environment is limited to 16GB RAM, 2 CPU cores and 50GB of (not persistent) disk space by default." (**đã kiểm**)
- Bảng giá: CPU Basic = 2 vCPU / 16 GB / **FREE**; CPU Upgrade = 8 vCPU / 32 GB / **$0.03/giờ**; Nvidia T4-small = 4 vCPU / 15 GB / 16 GB VRAM / **$0.40/giờ**; A100-large **$2.50/giờ** (**đã kiểm**)
- **Chốt chặn mới:** "Gradio and Docker Spaces run on compute and require a paid plan to create: PRO for personal accounts, Team or Enterprise for organizations. Free personal accounts in good standing can still host up to 2 Gradio Spaces running on ZeroGPU." Static Spaces "are free for everyone." (**đã kiểm**)
- Ngủ đông: "On free hardware, your Space will 'go to sleep' and stop executing after a period of time if unused." "Paused time is not billed." (**đã kiểm**)
- Networking: chỉ port 80, 443, 8080 ra ngoài; "Any requests going to other ports will be blocked." (**đã kiểm**)
- Persistent storage: **$12/TB/tháng** repo public, **$18/TB/tháng** private (**đã kiểm**)

**HuggingFace ZeroGPU** — [spaces-zerogpu](https://huggingface.co/docs/hub/spaces-zerogpu) (đọc 01/10/2026)
- Phần cứng: `large` (mặc định) = nửa NVIDIA RTX Pro 6000 Blackwell, **48 GB VRAM**, quota cost 1×; `xlarge` = full card, 96 GB, quota cost 2× (**đã kiểm**)
- **Quota GPU theo ngày, theo tài khoản người xem:** Unauthenticated **2 phút/ngày** (ưu tiên thấp); Free account **5 phút/ngày** (trung bình); PRO **40 phút/ngày** (có thể mở rộng, ưu tiên cao nhất); Enterprise 60 phút/ngày. "Included daily quota resets exactly 24 hours after your first GPU usage." (**đã kiểm**)
- Mở rộng quota: PRO/Team/Enterprise mua thêm ở mức **$1 cho 10 phút GPU** (**đã kiểm**)
- Hạn chế kỹ thuật: "ZeroGPU Spaces are exclusively compatible with the **Gradio SDK**"; PyTorch 2.8.0→mới nhất; **không hỗ trợ `torch.compile`** (chỉ AOT compilation); mặc định **60 giây** GPU runtime mỗi hàm, mở rộng bằng `@spaces.GPU(duration=120)` (**đã kiểm**)
- Model phải nạp lên `cuda` **ở module level**, không lazy-load trong hàm: "Lazy-loading or moving models to CUDA inside `@spaces.GPU` is discouraged, as it is significantly less efficient." (**đã kiểm**)
- Giới hạn host: free personal **tối đa 2 ZeroGPU Space**, điều kiện "verified email, account older than 30 days"; PRO tối đa 10 (**đã kiểm**)

**Google Cloud Run** — [memory limits docs](https://docs.cloud.google.com/run/docs/configuring/services/memory-limits) (đọc 01/10/2026)
- "The maximum amount of memory you can configure is 32 gibibyte (`32 Gi`)." (**đã kiểm**)
- "By default, the memory allocated to each instance of a revision is 512 MiB." (**đã kiểm**)
- Bảng CPU↔RAM: .08 vCPU → tối đa 512 MiB; 1 vCPU → tối đa 4 GiB; 2 vCPU → tối đa 8 GiB; 4 vCPU → 2–16 GiB; 8 vCPU → 4–32 GiB (**đã kiểm**)
- Minimum: "128 MiB for first generation" và "512 MiB for second generation" (**đã kiểm**)

**Render** — [render.com/docs/free](https://render.com/docs/free) (đọc 01/10/2026)
- "Render **spins down** a Free web service that goes 15 minutes without receiving any inbound traffic." Khôi phục mất **~1 phút**, trong lúc đó hiện trang loading (**đã kiểm**)
- "Render grants **750 Free instance hours** to each workspace per calendar month." (**đã kiểm**)
- "Free web services _cannot_" dùng persistent disk (**đã kiểm**)
- Free Postgres: "Fixed storage capacity of 1 GB", "Free Render Postgres databases expire 30 days after creation", 1 DB/workspace (**đã kiểm**)
- Free Key Value (Redis): "In-memory only", không ghi đĩa, dữ liệu "lost" khi instance restart, 1 instance/workspace (**đã kiểm**)

**Fly.io** — [docs.fly.io/about/pricing](https://docs.fly.io/about/pricing/) (đọc 01/10/2026)
- Shared-CPU preset từ shared-cpu-1x đến shared-cpu-8x, RAM 256 MB → 16 GB (**đã kiểm**)
- Tài liệu **không nêu free machine allowance** cho shared-CPU (**đã kiểm** — tức free tier cũ đã không còn trong trang giá)
- Máy đã stop: "For stopped Machines we charge only for the root file system (rootfs) needed for each Machine. Each 1GB of rootfs for a Machine stopped for 30 days is $0.15." (**đã kiểm**)
- Volume: "$0.15/GB per month of provisioned capacity", tính theo giờ pro-rated bất kể máy có chạy hay không (**đã kiểm**)
- Egress: Bắc Mỹ/Âu **$0.02/GB**; APAC/Oceania/Nam Mỹ **$0.04/GB**; Phi/Ấn **$0.12/GB** (**đã kiểm**)

**Modal (serverless, trả theo giây)** — [modal.com/pricing](https://modal.com/pricing) (đọc 01/10/2026)
- CPU **$0.0000131 / core / giây**; Memory **$0.00000222 / GiB / giây** (**đã kiểm**)
- GPU/giây: T4 **$0.000164**; L4 **$0.000222**; A10 **$0.000306**; A100-40GB **$0.000583**; A100-80GB **$0.000694**; H100 SXM5 **$0.001097** (**đã kiểm**)
- Credit miễn phí: Starter Plan **$30/tháng free credits**; Team Plan $100/tháng (**đã kiểm**)
- Tối thiểu: "minimum of 0.125 cores per container" và 128 MiB RAM/container (**đã kiểm**)

**Kaggle / Colab (compute nghiên cứu, KHÔNG phải host)**
- Kaggle: quota GPU **30 giờ/tuần** (có "floating quota" đôi khi cao hơn tùy tải hệ thống); GPU là NVIDIA P100 16 GB hoặc T4 (T4×2 = 32 GB VRAM ở beta); session tối đa **12 giờ** CPU/GPU, 9 giờ TPU — [Kaggle: Efficient GPU Usage](https://www.kaggle.com/docs/efficient-gpu-usage), [Kaggle product-feedback: floating GPU quota](https://www.kaggle.com/product-feedback/173129) (**đã kiểm**)
- Liên kết Colab Pro cho thêm 15 giờ GPU/tuần, Pro+ cho thêm 30 giờ/tuần — [Kaggle blog](https://www.kaggle.com/blog/level-up-your-compute-more-gpu-hours-on-kaggle-wit) (**đã kiểm**)

### Inferences

**Chi phí Modal ở mức 100 request/ngày (suy luận, phép tính viết rõ):**

Giả định mỗi request chiếm 30 s wall-clock trên 2 core + 4 GiB RAM (giả định này **chưa kiểm**, cần benchmark):
- CPU: 30 s × 2 core × $0.0000131 = **$0,000786**
- RAM: 30 s × 4 GiB × $0.00000222 = **$0,0002664**
- Tổng/request ≈ **$0,00105**
- 100 req/ngày × 30 ngày = 3 000 req/tháng → 3 000 × $0,00105 = **$3,16/tháng**
- → **Nằm hoàn toàn trong $30 credit free của Starter Plan.** Chi phí thực tế = **$0**.

Nếu dùng GPU T4 thay vì CPU, giả định 3 s GPU/request:
- 3 s × $0.000164 = $0,000492/request → 3 000 req = **$1,48/tháng** → cũng trong credit free.
- **suy luận quan trọng:** với Modal, **GPU rẻ hơn CPU** cho workload này, vì GPU rút ngắn wall-clock đủ nhiều để bù giá/giây. Đây là luận điểm phản trực giác nhưng có cơ sở số học, dùng được khi bảo vệ.

**Quota ZeroGPU ở mức 100 request/ngày (suy luận):**
- Quota là **theo người xem**, không theo Space. 100 request/ngày từ, giả sử, 20 người xem khác nhau → mỗi người ~5 request. Khách không đăng nhập có 2 phút = 120 s/ngày → 5 request × ~10 s = 50 s, **vừa quota**. Một người dùng duy nhất bắn 100 request/ngày thì cần 1 000 s ≈ 16,7 phút GPU → **vượt** quota free 5 phút và vượt cả PRO 40 phút nếu mỗi request >24 s.
- → ZeroGPU **phù hợp cho demo nhiều người dùng lẻ**, **không phù hợp cho batch của một người**. Phải thiết kế: demo tương tác dùng ZeroGPU, batch lớn thì xuất file để chạy trên Kaggle.

**Bảng tổng hợp khả năng host (suy luận, dựa trên các số đã kiểm ở trên):**

| Host | RAM/CPU | Cold start | Nạp được model nhiều GB? | Storage bền | Chi phí @100 req/ngày |
|---|---|---|---|---|---|
| HF Spaces CPU Basic | 2 vCPU / 16 GB / 50 GB đĩa tạm | Ngủ sau một thời gian không dùng → phải tải lại trọng số | **Có** (16 GB RAM) | Không (đĩa không bền; $12/TB/mo nếu mua) | **$0** nhưng **cần PRO để tạo Docker/Gradio Space** |
| HF ZeroGPU (Gradio) | 48 GB VRAM, giới hạn 60 s/hàm | Có, cộng thời gian xếp hàng | **Có** | Không | **$0** trong quota 5 phút/ngày/người |
| Cloud Run | mặc định 512 MiB, tối đa 32 GiB (8 vCPU) | Có (scale-to-zero) | **Có** nếu cấu hình ≥4 vCPU/16 GiB | Không (cần GCS) | Free tier **chưa kiểm** (xem Gaps) |
| Render Free | **chưa kiểm RAM** | **~1 phút** sau 15 phút idle | Khả năng cao **không** | **Không** (không có disk) | $0 trong 750 giờ/tháng |
| Fly.io | 256 MB–16 GB | auto-start có cold start | Tùy preset | $0.15/GB/mo | **Không còn free tier trong trang giá** |
| Modal | 0,125 core–nhiều, RAM tùy | Có, nhưng nạp model vào image/volume giảm được | **Có** | Có (Volume) | **$0** (trong $30 credit) |
| Oracle Always Free ARM | **chưa kiểm** (403) | Không (VM chạy liên tục) | **chưa kiểm** | Có | **chưa kiểm** |
| Vercel/Netlify | chỉ frontend static | n/a | Không | n/a | $0 |

- **suy luận:** Render free **không dùng được cho backend ML**: không có persistent disk (phải tải lại trọng số từ HF Hub sau mỗi lần spin-down), cold start ~1 phút, và Key Value free là in-memory-only nên **không thể làm job queue đáng tin** (mất job khi restart). Nếu chọn pattern background-job (mục 3), Redis free của Render là lựa chọn sai.
- **suy luận:** kiến trúc rẻ nhất và ổn định nhất trong ngân sách "vài chục USD": **frontend static trên Vercel/Netlify/HF Static Space ($0) + inference serverless trên Modal (trong $30 credit/tháng) + FAISS index nạp từ Modal Volume**. Phương án dự phòng: ZeroGPU Space (Gradio) nếu chịu được 2 Space và quota ngày.
- **Vượt ngân sách (đánh dấu rõ):** HF Spaces GPU thường trú T4-small ở $0.40/giờ × 24 × 30 = **$288/tháng** → **vượt xa** ngân sách "vài chục USD". A100-large $2.50/giờ → $1 800/tháng. Không bao giờ đưa vào đề cương như phương án mặc định.

### Gaps

- **Cloud Run free tier (vCPU-giây, GiB-giây, số request/tháng miễn phí)**: trang `cloud.google.com/run/pricing` bị truncate khi fetch, không lấy được số. **Phải đọc lại trực tiếp** trước khi viết đề cương.
- **Oracle Cloud Always Free (Ampere A1 ARM OCPU/RAM/block storage)**: `oracle.com/cloud/free` trả HTTP 403. Đây là lựa chọn đáng tiếc nhất bị thiếu, vì 4 OCPU ARM + 24 GB RAM (nếu con số đó còn đúng) sẽ là host CPU-only *thường trú, miễn phí* tốt nhất cho đúng bài toán này — **ưu tiên số 1 để kiểm lại**.
- **RAM/CPU cụ thể của Render free web service**: trang docs/free không nêu.
- **Giá gói HuggingFace PRO/tháng**: không đọc được trong phiên này, nhưng nó quyết định liệu Docker Space có khả thi hay không.
- **Railway**: không kiểm được trong phiên này (free tier/trial credit/Hobby plan).
- **Replicate, Banana-style serverless GPU**: không kiểm được giá/giây trong phiên này.
- **Bandwidth miễn phí của Render**: docs nói "count against your monthly included amounts" mà không nêu số.

---

## 3. Pattern kiến trúc cho inference chậm phía sau web UI

### Takeaway

FastAPI docs nói thẳng điều cần trích vào đề cương: `BackgroundTasks` dành cho việc nhẹ, còn "heavy background computation" thì nên dùng Celery + Redis/RabbitMQ. Và các web server tin sinh thật đã công bố hạn mức submission rất cụ thể (NetSurfP, DeepTMHMM) — đây là nguồn trích dẫn tốt để biện minh cho giới hạn chống lạm dụng, chứ không phải tự đặt ra.

### Cited Findings

**FastAPI BackgroundTasks vs Celery** — [FastAPI: Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) (đọc 01/10/2026), trích nguyên văn mục "Caveat":
> "If you need to perform heavy background computation and you don't necessarily need it to be run by the same process (for example, you don't need to share memory, variables, etc), you might benefit from using other bigger tools like Celery. They tend to require more complex configurations, a message/job queue manager, like RabbitMQ or Redis, but they allow you to run background tasks in multiple processes, and especially, in multiple servers. But if you need to access variables and objects from the same FastAPI app, or you need to perform small background tasks (like sending an email notification), you can simply just use `BackgroundTasks`."
(**đã kiểm**)

**Hạn mức submission đã công bố của web server tin sinh thật**
- **NetSurfP-3.0**: tối đa **10 000 chuỗi**, độ dài **10–5 000 residue** mỗi chuỗi, hoặc tổng **10 triệu residue**; nếu gặp lỗi out-of-memory thì phải bỏ hết chuỗi >1 022 residue, và loại chuỗi dài đó chỉ nộp được **tối đa 40 chuỗi một lần** — [NetSurfP-3.0, DTU Health Tech](https://services.healthtech.dtu.dk/services/NetSurfP-3.0/) (**đã kiểm**, qua tổng hợp trang service)
- **NetSurfP-2.0**: tối đa **100 chuỗi** hoặc tổng **100 000 residue** — [NetSurfP-2.0, DTU Health Tech](https://services.healthtech.dtu.dk/services/NetSurfP-2.0/) (**đã kiểm**)
- **DeepTMHMM**: tối đa **10 000 chuỗi protein** mỗi lần nộp — [DeepTMHMM 1.0, DTU Health Tech](https://services.healthtech.dtu.dk/services/DeepTMHMM-1.0/) (**đã kiểm**)

**Hạ tầng queue trên free tier (cảnh báo từ mục 2)**
- Render free Key Value: "In-memory only", dữ liệu "lost" khi instance restart — [render.com/docs/free](https://render.com/docs/free) (**đã kiểm**)

### Inferences

- **suy luận:** NetSurfP-2.0 → 3.0 là **bằng chứng tiến hoá** trực tiếp dùng được trong đề cương: khi chuyển từ model cũ sang model dựa trên PLM, hạn mức **tăng 100×** (100 chuỗi → 10 000 chuỗi) *nhưng* xuất hiện thêm một hạn mức mới theo **độ dài** (>1 022 residue chỉ 40 chuỗi/lần). Đó chính là dấu vết của O(L²) attention memory trong thiết kế hệ thống thật. Đề tài có thể trích làm căn cứ cho chính sách giới hạn của mình, thay vì bịa số.
- **suy luận về giới hạn nên đặt cho đề tài này**, lấy NetSurfP-3.0 làm mốc rồi chia tỉ lệ xuống theo hạ tầng free (phép tính: NetSurfP-3.0 chạy trên hạ tầng DTU có GPU; ta có ~1/100 compute): đề xuất **tối đa 20 chuỗi/lần nộp, mỗi chuỗi 30–1 000 residue, tổng ≤ 10 000 residue/lần**, rate limit theo IP. Mọi số này là **suy luận**, phải chốt lại sau khi có benchmark CPU thật.
- **suy luận:** chuỗi pattern tối thiểu cần thiết, xếp theo mức độ "đóng góp luận văn" so với "plumbing":
  1. **Plumbing (không phải đóng góp):** job-ID + polling, `BackgroundTasks` cho job nhẹ, rate limit, max-length cap, Docker compose. Đây là code phải viết nhưng không phải nội dung nghiên cứu.
  2. **Plumbing nhưng cần viết rõ trong chương Thiết kế:** cache kết quả theo **hash của chuỗi** (SHA-256 của chuỗi đã chuẩn hoá) — biến request trùng thành O(1); dedup request đang chạy bằng cách khoá theo cùng hash để 2 người nộp cùng protein chỉ chạy 1 lần.
  3. **Có tiềm năng là đóng góp:** chính sách **precompute**. Vì reference DB là tập huấn luyện đã biết, embedding + điểm dự đoán cho toàn bộ nó có thể tính sẵn **trên Kaggle (30 giờ GPU/tuần free)** rồi chỉ ship index + bảng kết quả. Request mới chỉ còn phải embed 1 chuỗi + truy vấn k-NN. Phần "quyết định cái gì precompute, cái gì tính nóng, dưới ràng buộc quota" là một bài toán thiết kế có thể định lượng (hit rate vs. dung lượng index vs. latency) → **đủ sức làm một RQ**.
- **suy luận:** SSE đơn giản hơn WebSocket cho trường hợp này (một chiều server→client, chỉ báo tiến độ) và đi qua được proxy HTTP bình thường, trong khi ZeroGPU/Gradio đã có sẵn cơ chế queue riêng nên nếu chọn ZeroGPU thì **không nên tự xây queue** — Gradio làm việc đó. Nếu chọn Modal thì Modal có `spawn()`/`FunctionCall.get()` tức job-ID polling có sẵn. Tức là: **chọn host trước, pattern queue sẽ gần như bị quyết định theo**. Đây là luận điểm thiết kế nên nói rõ với GVHD.
- **suy luận:** Redis free của Render in-memory-only nghĩa là nếu dùng Celery/RQ/arq trên free tier, một lần restart host sẽ **mất hết job đang chờ**. Hệ quả thiết kế: job-ID result URL phải **persist ở nơi khác** (Postgres free 1 GB của Render, hoặc Modal Volume, hoặc chỉ cần một file JSON trên volume), và client phải chịu được "job biến mất" → phải cho phép nộp lại idempotent theo hash chuỗi. Đây là một ràng buộc *thật* do free tier gây ra, và viết nó ra là một phần của "defend the architecture".

### Gaps

- **Không tìm được** tài liệu kỹ thuật công khai nào của một web server tin sinh thật **mô tả kiến trúc queue nội bộ** (Celery vs. gì khác). Các trang service chỉ công bố *hạn mức*, không công bố *kiến trúc*. Nếu cần nguồn cho pattern, phải dựa vào docs của framework (FastAPI/Celery/arq) chứ không có "bioinformatics precedent" trích được.
- Không đọc được docs của **Celery / arq / RQ** trong phiên này (hết budget tool call) — các mệnh đề về chúng ở trên đều lấy từ chính FastAPI docs, không phải từ docs gốc của chúng.
- Chưa kiểm được rate-limit middleware cụ thể nào (slowapi, fastapi-limiter) và giới hạn của chúng trên serverless (nơi state in-memory không chia sẻ giữa các instance) — đây là một vấn đề kỹ thuật thật: **rate limit trên serverless cần backing store ngoài**, chưa có nguồn.

---

## 4. Kỹ thuật FAISS / vector index

### Takeaway

Ở 200k–500k vector × 1024 dim, **Flat index nằm trong khoảng 0,82–2,05 GB RAM** — tức vẫn vừa free tier 16 GB của HF Spaces nhưng **không vừa** host 512 MB–2 GB. PQ nén được **64×** xuống còn 12,8–32 MB. Và điểm then chốt cho RQ "cập nhật DB thay vì huấn luyện lại model": **chỉ `IndexFlat` là add được mà không cần train**; mọi index còn lại (IVF, PQ, LSH) đều cần train trước — nhưng train là train *quantizer*, **không phải train lại PLM hay CNN head**, nên luận điểm của RQ vẫn đứng được, chỉ cần phát biểu chính xác.

### Cited Findings

**Công thức bộ nhớ** — [FAISS wiki: Guidelines to choose an index](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index) và [FAISS wiki: Faiss indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes) (đọc 01/10/2026)
- Flat: `4*d` bytes/vector, không nén, không cần train, tìm kiếm **chính xác** (brute-force) (**đã kiểm**)
- IndexIVFFlat: `4*d + 8` bytes/vector, xấp xỉ (**đã kiểm**)
- HNSW: `(d * 4 + M * 2 * 4)` bytes/vector, với M từ 4–64 (M cao hơn = chính xác hơn) (**đã kiểm**)
- PQ: `M` bytes/vector (M thường ≤ 64); PQ với mã 4-bit: `M/2` bytes/vector (**đã kiểm**)
- IndexIVFPQ: `ceil(M*nbits/8) + 8` bytes/vector (**đã kiểm**)
- IndexLSH: `ceil(nbits/8)` bytes/vector (**đã kiểm**)
- RaBitQ (nén 1-bit): `(d/8 + 8)` bytes/vector (**đã kiểm**)

**Chọn index theo kích thước dataset** — [FAISS: Guidelines to choose an index](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index)
- **Dưới 1M vector:** `"...,IVF_K,..."` với **K = 4*sqrt(N) đến 16*sqrt(N)**; train cần **30 000 đến 256 000 vector** (**đã kiểm**)
- 1M–10M: `"...,IVF65536_HNSW32,..."`, train cần 1 966 080 đến 16 711 680 vector (**đã kiểm**)
- 10M–100M: `IVF262144_HNSW32`; 100M–1B: `IVF1048576_HNSW32` (**đã kiểm**)
- Điều chỉnh speed/accuracy: HNSW qua `efSearch`, IVF qua `nprobe`; "PQ with OPQ preprocessing improves compression accuracy" (**đã kiểm**)

**Yêu cầu train**
- Trang Guidelines: `"Flat"` không cần train; **"HNSW and SVSVamana require sequential adds only"**; "IVF variants require k-means clustering preprocessing"; "OPQ requires linear transformation training" (**đã kiểm**)
- Bảng trên trang "Faiss indexes" (qua fetch) lại ghi IndexHNSWFlat là **cần train** — **nguồn mâu thuẫn**, xem phần Inferences (**đã kiểm cả hai, mâu thuẫn**)
- Kiểm chéo mã nguồn `IndexHNSW.h`: có method `void train(idx_t n, const float* x) override;` với mô tả "Trains the storage if needed", tức train **có điều kiện theo storage backend**, và vector add được qua `add()` mà không cần gọi `train()` tường minh; subclass `IndexHNSWPQ` override train vì PQ mới thực sự cần — [faiss/IndexHNSW.h](https://github.com/facebookresearch/faiss/blob/main/faiss/IndexHNSW.h) (**đã kiểm**)

### Inferences

**Bộ nhớ index ở d = 1024 (suy luận, phép tính viết rõ):**

| Index | Bytes/vector | N = 200 000 | N = 500 000 |
|---|---|---|---|
| Flat | 4×1024 = **4 096 B** | 200 000×4 096 = 819,2 MB → **0,82 GB** | 500 000×4 096 = 2 048 MB → **2,05 GB** |
| IVFFlat | 4×1024+8 = **4 104 B** | **820,8 MB** | **2 052 MB (2,05 GB)** |
| HNSW, M=32 | 1024×4 + 32×2×4 = 4 096+256 = **4 352 B** | **870,4 MB** | 2 176 MB → **2,18 GB** |
| HNSW, M=64 | 4 096 + 64×2×4 = **4 608 B** | **921,6 MB** | **2 304 MB (2,30 GB)** |
| PQ, M=64, 8 bit | **64 B** | **12,8 MB** | **32,0 MB** |
| IVFPQ, M=64, 8 bit | 64+8 = **72 B** | **14,4 MB** | **36,0 MB** |
| PQ 4-bit, M=64 | 64/2 = **32 B** | **6,4 MB** | **16,0 MB** |
| RaBitQ (1-bit) | 1024/8+8 = **136 B** | **27,2 MB** | **68,0 MB** |

- **Tỉ lệ nén (suy luận):** PQ M=64 nén **4 096/64 = 64×** so với Flat. PQ 4-bit nén **128×**. RaBitQ nén **4 096/136 ≈ 30×**.
- **nlist nên dùng (suy luận từ công thức K = 4√N…16√N của FAISS):**
  - N = 200 000: √200 000 ≈ 447,2 → K từ 4×447,2 = **1 789** đến 16×447,2 = **7 155**. Factory string ví dụ `IVF2048,Flat` hoặc `IVF4096,PQ64`.
  - N = 500 000: √500 000 ≈ 707,1 → K từ **2 828** đến **11 314**. Ví dụ `IVF4096,Flat` hoặc `IVF8192,PQ64`.
  - Cả hai trường hợp đều **dưới 1M** nên theo guideline chỉ cần IVF_K thuần, **không cần** `IVF..._HNSW32` (cái đó dành cho ≥1M).
- **Train set (suy luận):** guideline yêu cầu 30 000–256 000 vector để train. Với N = 200 000 thì train set 30k–200k nghĩa là **có thể train trên chính toàn bộ reference DB**, không cần sampling đặc biệt. Với N = 500 000, sample 256 000 là đủ theo trần guideline.
- **Về RQ "cập nhật DB thay vì huấn luyện lại model" (suy luận, điểm quan trọng nhất của mục này):**
  - `IndexFlat` **add được vô hạn, không cần train, không mất recall** → là index "updatable" hoàn hảo, giá phải trả là RAM tuyến tính (2,05 GB ở 500k) và latency truy vấn tuyến tính.
  - `IndexHNSW` add được tuần tự không cần train (theo trang Guidelines + mã nguồn), nhưng không xoá được vector và chất lượng graph suy giảm nếu phân phối dữ liệu mới lệch so với dữ liệu cũ (mệnh đề suy giảm này **chưa kiểm**).
  - `IndexIVF*` và `IndexPQ`: train xong **vẫn add thêm được** (`add()` hoạt động sau `train()`); vấn đề là centroid/codebook được fit trên phân phối cũ, nên vector mới ngoài phân phối sẽ bị quantize tệ.
  - → **Phát biểu RQ cần chính xác hơn:** không phải "FAISS index nào add được", mà là **"thêm vector mới vào index đã train làm recall suy giảm bao nhiêu, và khi nào buộc phải re-train quantizer?"** Đây là câu hỏi **đo được**, có baseline rõ (so với Flat exact search làm ground truth), chạy được trên CPU, và **chưa thấy ai trả lời cho embedding protein per-residue**. Nếu đúng vậy thì đây là RQ mạnh nhất trong toàn bộ ghi chú này — vì nó vừa là nghiên cứu, vừa là ràng buộc triển khai thật, vừa chạy được không cần GPU.
- **suy luận:** chiến lược hai tầng khả thi trên free tier: giữ **IVFPQ (36 MB)** làm index chính để truy vấn nhanh trong RAM nhỏ, cộng **re-rank exact** trên top-k ứng viên bằng cách đọc embedding gốc từ đĩa/memmap. Vậy RAM thường trú chỉ 36 MB thay vì 2,05 GB — giảm **~57×** (2 052/36). Đây là pattern đáng viết vào chương Thiết kế.

### Gaps

- **Không tìm được số recall loss cụ thể của PQ** (ví dụ recall@10 giảm bao nhiêu % ở M=64, 8-bit, d=1024). FAISS wiki nói về tradeoff nhưng không cho bảng số trong phần tôi đọc được. Phải tự đo (và việc tự đo chính là nội dung RQ ở trên).
- **Không tìm được số build time** cho IVF/HNSW/PQ ở 200k–500k × 1024d trên CPU. Phải tự đo.
- **Không tìm được số query latency** (ms/truy vấn) cho các index này. Phải tự đo.
- **Mâu thuẫn nguồn chưa giải quyết hoàn toàn:** trang "Guidelines to choose an index" nói HNSW chỉ cần "sequential adds", trong khi bảng trên trang "Faiss indexes" (như bản fetch trả về) đánh HNSWFlat là cần train. Mã nguồn nghiêng về "train có điều kiện, không bắt buộc". **Nên kiểm trực tiếp bằng code** (`faiss.IndexHNSWFlat(1024, 32).is_trained`) thay vì tin tài liệu — mất 1 phút và chấm dứt tranh cãi.
- Chưa kiểm được FAISS có hỗ trợ `remove_ids` trên những index nào (quan trọng nếu reference DB cần xoá entry).

---

## 5. Chi phí vận hành lớp LLM

### Takeaway

Lớp LLM **không phải là vấn đề chi phí**: 1 000 explanation ở mức 2 000 input / 300 output token tốn từ **$0,22** (gpt-5-nano) đến **$3,50** (Claude Haiku 4.5), và Gemini có free tier thật (500 RPD). Ngược lại, **self-host LLM nhỏ trên CPU là không khả thi cho UX đồng bộ**: ở 4 tok/s thì 300 token output mất **75 giây**.

### Cited Findings

**Google Gemini** — [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing) (đọc 01/10/2026)
- **Gemini 2.5 Flash-Lite**: free tier "Free of charge, up to 500 RPD"; paid **$0.10/1M input** (text/image/video), **$0.40/1M output** (**đã kiểm**)
- **Gemini 2.5 Flash**: free tier "Free of charge" với giới hạn **500 RPD**; paid **$0.30/1M input**, **$2.50/1M output** (**đã kiểm**)
- **Gemini 3.5 Flash-Lite**: paid $0.30/1M input, $2.50/1M output; có free tier (**đã kiểm**)
- **Gemini 3.8 Flash**: paid "$0.75 through December 31, 2026. $1.50 starting January 1, 2027" input; "$3.75 through December 31, 2026. $7.50 starting January 1, 2027" output (**đã kiểm** — lưu ý giá **tăng gấp đôi từ 01/01/2027**, trùng với thời gian làm luận văn)
- Mọi free tier đều kèm "Limited access to certain models" và dữ liệu "potentially used to improve products" (**đã kiểm** — có ý nghĩa nếu dữ liệu đầu vào là chuỗi protein chưa công bố)

**OpenAI** — [developers.openai.com/api/docs/pricing](https://developers.openai.com/api/docs/pricing) (đọc 01/10/2026)
- **gpt-5-nano**: **$0.05/1M input**, **$0.40/1M output** (**đã kiểm**) — rẻ nhất tìm được
- **gpt-4o-mini**: **$0.15/1M input**, **$0.60/1M output** (**đã kiểm**)
- **gpt-5.4-nano**: $0.20/1M input, $1.25/1M output (**đã kiểm**)

**Anthropic** — bảng giá cached 2026-09-25 trong skill `claude-api` của Claude Code (nguồn nội bộ, không phải link web)
- **Claude Haiku 4.5** (`claude-haiku-4-5`): **$1.00/1M input**, **$5.00/1M output**, context 200K (**đã kiểm** từ bảng trong skill; giá đối chiếu tại [anthropic.com/pricing](https://www.anthropic.com/pricing) — **chưa fetch trực tiếp trong phiên này**)
- Không thấy đề cập free tier cho Claude API (**đã kiểm** theo nghĩa: tài liệu không nêu; không phải bằng chứng khẳng định là không có)

**llama.cpp / Ollama trên CPU** — các nguồn thứ cấp, độ tin cậy thấp hơn
- 7B Q4_K_M trên CPU desktop nhanh (Ryzen 7 7700X): **~5–10 tok/s**; dải chung cho 3B–7B Q4_K_M: **4–15 tok/s** — [promptquorum: CPU-Only LLM 2026](https://www.promptquorum.com/local-llms/best-cpu-only-llm), [markaicode: Ollama CPU benchmark](https://markaicode.com/benchmarks/tool-cpu-benchmark/) (**đã kiểm nhưng là blog, không phải nguồn gốc**)
- Llama 3.1 8B Q4_K_M, 12 thread trên core AMD EPYC: **14,2 tok/s** — [presenc.ai: Local LLM tokens-per-second benchmarks 2026](https://presenc.ai/research/local-llm-tokens-per-second-benchmarks-2026) (**đã kiểm**, nguồn thứ cấp)
- Llama 2 Chat 7B Q4_K_M trên **4 vCPU Intel Xeon**: **4,06 tok/s**; Mistral 7B cùng máy: **3,64 tok/s** — [cùng nguồn](https://presenc.ai/research/local-llm-tokens-per-second-benchmarks-2026) (**đã kiểm**, nguồn thứ cấp — con số 4 vCPU Xeon là mốc gần nhất với free tier thật)

### Inferences

**Chi phí 1 000 explanation (suy luận, phép tính viết rõ).** Tổng token: 1 000 × 2 000 = **2 000 000 input = 2,0 MTok**; 1 000 × 300 = **300 000 output = 0,3 MTok**.

| Model | Tính input | Tính output | **Tổng 1 000 explanation** |
|---|---|---|---|
| gpt-5-nano | 2,0 × $0,05 = $0,10 | 0,3 × $0,40 = $0,12 | **$0,22** |
| Gemini 2.5 Flash-Lite (paid) | 2,0 × $0,10 = $0,20 | 0,3 × $0,40 = $0,12 | **$0,32** |
| gpt-4o-mini | 2,0 × $0,15 = $0,30 | 0,3 × $0,60 = $0,18 | **$0,48** |
| Gemini 2.5 Flash (paid) | 2,0 × $0,30 = $0,60 | 0,3 × $2,50 = $0,75 | **$1,35** |
| Claude Haiku 4.5 | 2,0 × $1,00 = $2,00 | 0,3 × $5,00 = $1,50 | **$3,50** |
| Gemini 2.5 Flash free tier | — | — | **$0,00** (nhưng cần ≥2 ngày vì 500 RPD) |

- **suy luận:** 1 000 explanation ở mức 500 RPD của Gemini free tier cần **1 000/500 = 2 ngày**. Toàn bộ pha thí nghiệm của luận văn (kể cả 10 000 explanation) chạy được **miễn phí** trong 20 ngày, hoặc **$2,20–$35** nếu trả tiền. → **Lớp LLM không phải rào cản ngân sách.** Rào cản là lớp PLM.
- **suy luận:** ở mức 100 request/ngày trong production demo, 100 × 30 = 3 000 explanation/tháng → gpt-5-nano: 3× $0,22 = **$0,66/tháng**. Hoàn toàn trong ngân sách "vài chục USD".
- **suy luận về self-host trên CPU:** lấy mốc đo gần nhất với free tier (4 vCPU Xeon, 7B Q4_K_M, **4,06 tok/s**):
  - 300 token output / 4,06 tok/s = **73,9 giây** chỉ cho phần generation.
  - Cộng prompt processing 2 000 token input: nếu prefill nhanh hơn generation ~5× (tỉ lệ này **chưa kiểm**) thì ~2 000/20 = 100 s nữa → **tổng ~3 phút/explanation**.
  - → **Không khả thi cho UX đồng bộ**, và cũng không đáng: $0,22 cho 1 000 explanation qua API rẻ hơn mọi chi phí thời gian của self-host.
- **suy luận về RAM cho quantized LLM:** 7B tham số ở Q4_K_M (~4,5 bit/tham số trung bình): 7e9 × 4,5/8 = **3,94 GB** trọng số, cộng KV cache. Vừa 16 GB của HF Spaces nhưng **không vừa** 512 MB–2 GB. (Con số 4,5 bit/tham số của Q4_K_M là **chưa kiểm**.)
- **suy luận quan trọng cho đề cương:** vì API LLM rẻ và có free tier, **lớp thứ hai (giải thích có citation) không nên là nơi đặt đóng góp kỹ thuật về hiệu năng**. Đóng góp ở lớp này phải là về **grounding/đánh giá** (ví dụ: tỉ lệ câu có citation hợp lệ, tỉ lệ bịa citation), chứ không phải về chi phí hay tốc độ.

### Gaps

- **Không fetch được trực tiếp** [anthropic.com/pricing](https://www.anthropic.com/pricing) trong phiên này; giá Haiku 4.5 lấy từ bảng cached (2026-09-25) trong skill nội bộ. Cần kiểm lại nếu đưa vào đề cương.
- Rate limit cụ thể của free tier Gemini ngoài "500 RPD" (RPM, TPM) chưa kiểm.
- **Không có benchmark llama.cpp từ nguồn gốc** (repo `ggml-org/llama.cpp` discussions) — mọi số tok/s ở trên đều từ blog tổng hợp. Độ tin cậy thấp; nếu cần số đáng trích thì phải đọc [llama.cpp discussion #4167](https://github.com/ggml-org/llama.cpp/discussions/4167) hoặc tự đo bằng `llama-bench` trên WSL2.
- Chưa kiểm giá của các provider mở rẻ khác (Groq, Together, DeepInfra, OpenRouter) vốn có thể rẻ hơn gpt-5-nano.
- Chưa kiểm liệu free tier của Gemini có **điều khoản nào cấm dùng trong nghiên cứu/luận văn** hay yêu cầu ghi nhận.

---

## 6. Tái lập và đóng gói

### Takeaway

Phần này là mục **yếu nhất về nguồn** trong ghi chú — tôi đã hết budget tool call trước khi kiểm được các pattern Docker/CI. Những gì **đã kiểm** đều là ràng buộc từ phía host (đĩa không bền, giới hạn port, giá storage), và chúng đủ để suy ra một quyết định rõ: **phân phối trọng số qua HuggingFace Hub với revision pin, không đưa vào git**.

### Cited Findings

- HF Spaces: "50GB of (not persistent) disk space by default" — [spaces-overview](https://huggingface.co/docs/hub/spaces-overview) (**đã kiểm**). Tức trọng số tải về sẽ **mất sau mỗi lần Space ngủ/rebuild**.
- HF Spaces persistent storage có giá: **$12/TB/tháng** public, **$18/TB/tháng** private (**đã kiểm**)
- HF Spaces chỉ mở port 80/443/8080 ra ngoài; "Any requests going to other ports will be blocked." — [spaces-overview](https://huggingface.co/docs/hub/spaces-overview) (**đã kiểm**). Ảnh hưởng trực tiếp đến docker-compose nhiều service.
- Spaces lưu code trong git repo, dùng `git` và `git-xet`; "Each time a new commit is pushed, the Space will automatically rebuild and restart." — [cùng nguồn](https://huggingface.co/docs/hub/spaces-overview) (**đã kiểm**)
- Space có thể khai báo model/dataset phụ thuộc trong YAML metadata của README (`models:`, `datasets:`) — [cùng nguồn](https://huggingface.co/docs/hub/spaces-overview) (**đã kiểm**). Đây là cơ chế khai báo phụ thuộc mô hình chính thức, dùng được cho mục tái lập.
- ZeroGPU chỉ hỗ trợ **Gradio SDK**, PyTorch 2.8.0→mới nhất, Python 3.12.12 hoặc 3.10.13, **không hỗ trợ `torch.compile`** — [spaces-zerogpu](https://huggingface.co/docs/hub/spaces-zerogpu) (**đã kiểm**). Đây là ràng buộc pin phiên bản rất cụ thể, trích được vào chương Triển khai.
- Modal: "minimum of 0.125 cores per container" và 128 MiB RAM/container — [modal.com/pricing](https://modal.com/pricing) (**đã kiểm**)
- Render free: "Free web services _cannot_" dùng persistent disk — [render.com/docs/free](https://render.com/docs/free) (**đã kiểm**)

### Inferences

- **suy luận:** cộng dồn các ràng buộc đã kiểm → **không được** commit trọng số PLM vào git repo của luận văn. Lý do: (a) Spaces rebuild lại mỗi commit, repo nặng làm rebuild chậm; (b) đĩa 50 GB không bền nên tải lại là bắt buộc dù sao; (c) HF Hub đã có sẵn trọng số và có cơ chế `revision` để pin. git-lfs hay release asset đều chỉ nhân bản dữ liệu đã có trên Hub.
- **suy luận:** cách pin phiên bản PLM đúng chuẩn là truyền commit SHA vào `revision=` của `from_pretrained` (cơ chế này tôi biết từ transformers API nhưng **chưa kiểm được bằng docs trong phiên này**), và ghi SHA đó vào file config của repo. Không pin thì "ProtT5-XL-U50" là một cái tên trỏ tới một mục tiêu di động → thí nghiệm không tái lập được.
- **suy luận:** docker-compose nhiều container (frontend + api + redis + ml-service) **không chạy được trên HF Spaces** vì chỉ 1 container và 3 port mở. Nếu muốn giữ compose cho phát triển cục bộ trên WSL2 mà vẫn deploy được, phải: compose cho dev + một Dockerfile đơn container (hoặc Gradio app) cho deploy → **hai artifact đóng gói khác nhau, phải nói rõ trong luận văn**, đừng giả vờ là một.
- **suy luận về CI không có GPU:** những việc CI *thực sự* chạy được miễn phí trên GitHub Actions runner CPU:
  1. Unit test logic (parse FASTA, hash chuỗi, validate độ dài, blending k-NN) — **không cần model nào**.
  2. Smoke test pipeline với **ESM-2 8M (32 MB fp32 theo tính toán ở mục 1)** làm stub thay cho ProtT5 — đủ nhỏ để tải trong CI.
  3. Test FAISS trên index tí hon (ví dụ 1 000 vector × 1024d = 1 000×4 096 = **4,1 MB**) và so recall của PQ với Flat exact → **chính là RQ ở mục 4, chạy được trong CI**.
  4. Kiểm tra ONNX export không crash + so sánh output với PyTorch trong tolerance, trên model stub.
  Mọi mệnh đề về giới hạn runner GitHub Actions (RAM/thời gian) ở đây đều **chưa kiểm**.
- **suy luận:** việc "CI chạy được RQ của mục 4 trên model stub" là một tính chất thiết kế đáng nhấn mạnh khi bảo vệ: nó chứng minh đóng góp nghiên cứu **không phụ thuộc GPU**, tức không phụ thuộc may mắn về hạ tầng.

### Gaps

- **Không kiểm được** tài liệu/ví dụ nào về pattern docker-compose cho "Python ML service + JS frontend" trong phiên này. Mục này gần như toàn bộ là suy luận.
- **Không kiểm được** docs của `transformers` về tham số `revision=` trong `from_pretrained` — cần đọc để trích đúng.
- **Không kiểm được** giới hạn của GitHub Actions free runner (RAM, phút/tháng cho repo private — lưu ý repo của đề tài **đã là private** từ 01/10/2026, nên phút CI bị tính vào quota, khác với repo public).
- **Không kiểm được** hướng dẫn hay ví dụ nào về ONNX export cho ProtT5/ESM-2 (có hỗ trợ sẵn trong `optimum` hay không, có giữ được chất lượng embedding hay không).
- Chưa kiểm model-weight distribution qua git-lfs/release assets có giới hạn dung lượng nào trên GitHub (quan trọng nếu quyết định ngược lại suy luận ở trên).

---

## 7. Vấn đề kỹ thuật nào đủ sức là đóng góp luận văn, cái nào chỉ là plumbing

### Takeaway

Trong toàn bộ những gì ghi chú này tìm được, chỉ có **hai** vấn đề đủ sức là đóng góp nghiên cứu, và cả hai đều đến từ **chính các khoảng trống số liệu** chứ không từ các pattern đã có sẵn.

### Inferences (toàn bộ mục này là suy luận, không có nguồn trực tiếp)

**Đủ sức là đóng góp:**
1. **Suy giảm recall khi thêm vector vào FAISS index đã train, cho embedding protein per-residue.** Lý do đủ mạnh: (a) FAISS wiki cho công thức bộ nhớ và ngưỡng chọn index nhưng **không cho số recall loss** (Gap mục 4); (b) có ground truth rõ ràng (Flat exact search); (c) chạy được hoàn toàn trên CPU, lặp lại được trong CI; (d) trả lời trực tiếp câu hỏi thực tiễn "cập nhật DB thay vì huấn luyện lại model được không, và được đến đâu". Phát biểu đúng phải là *"khi nào buộc re-train quantizer"*, không phải *"index nào add được"* (xem mục 4).
2. **Chính sách precompute dưới ràng buộc quota compute free.** Reference DB là tập huấn luyện đã biết → embedding tính sẵn được trên Kaggle (30 h GPU/tuần, **đã kiểm**). Bài toán: với ngân sách quota cố định, precompute cái gì để tối đa hoá tỉ lệ request được trả lời dưới ngưỡng latency? Định lượng được qua (hit rate, dung lượng index, p95 latency). Chưa thấy ai làm cho PLM + RAG per-residue.

**Chỉ là plumbing (phải làm, nhưng không phải nội dung nghiên cứu):**
- Job-ID + polling/SSE, rate limit, cap độ dài chuỗi, cache theo hash chuỗi, request dedup, Docker, CI, chọn host. Tất cả đều có pattern sẵn (FastAPI docs cho queue, DTU service pages cho hạn mức submission — cả hai **đã kiểm**). Viết vào chương Thiết kế, đừng viết vào chương Đóng góp.
- Lớp LLM giải thích: **không** đặt đóng góp về chi phí/tốc độ ở đây (1 000 explanation = $0,22–$3,50, có free tier 500 RPD — **đã kiểm**). Nếu muốn đóng góp ở lớp này thì phải là về **grounding và đánh giá citation**, không phải về engineering.

**Ranh giới cần nói rõ với GVHD:** việc benchmark CPU latency của PLM là **lấp khoảng trống đo lường** (không ai công bố số CPU — Gap mục 1), có giá trị kỹ thuật thật, nhưng một mình nó **chưa đủ** làm đóng góp luận văn vì nó là đo đạc chứ không phải phát hiện. Nó nên là *phương pháp* phục vụ hai RQ ở trên.

---

## Việc cần làm trước khi chốt kiến trúc trong đề cương

Xếp theo mức độ ảnh hưởng tới quyết định kiến trúc:

1. **Đọc lại Oracle Cloud Always Free** (403 trong phiên này). Nếu 4 OCPU ARM + 24 GB RAM thường trú miễn phí còn đúng, nó **đổi hẳn kiến trúc**: không cần serverless, không cần lo cold start, không cần ZeroGPU quota.
2. **Đọc lại Cloud Run free tier** (trang bị truncate). Quyết định liệu Cloud Run có là phương án dự phòng thật hay không.
3. **Tự benchmark trên WSL2**, ghi kết quả vào `ml/<slug>/experiments/`: thời gian CPU/protein 300 residue cho ProtT5 encoder fp32, ESM-2 650M, ESM-2 150M, ESM-C 300M; peak RSS cho từng cái; thời gian nạp trọng số. Đây là số **không ai công bố** (Gap mục 1) và là nền cho mọi quyết định còn lại.
4. **Chạy `faiss.IndexHNSWFlat(1024, 32).is_trained`** để dứt điểm mâu thuẫn nguồn ở mục 4 (1 phút).
5. **Đo recall/build time/query latency** cho Flat vs IVF vs HNSW vs IVFPQ ở 200k và 500k × 1024d trên CPU (Gap mục 4) — đây đồng thời là bước đầu của RQ số 1.
6. **Kiểm giá HuggingFace PRO/tháng** — quyết định Docker Space có khả thi hay không, và từ đó quyết định có phải chuyển sang Gradio+ZeroGPU hay không.
7. **Kiểm số llama.cpp từ nguồn gốc** nếu vẫn muốn giữ phương án self-host LLM trong đề cương (hiện mọi số đều từ blog thứ cấp).
