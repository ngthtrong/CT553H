# Đánh giá định lượng tầng giải thích LLM-RAG trong ngữ cảnh y sinh / protein

> Phạm vi: hệ thống web dự đoán residue gắn ATP trên receptor tyrosine kinase (RTK); tầng thứ hai truy hồi tài liệu (UniProt, PubMed abstract, InterPro/Pfam) và yêu cầu LLM sinh một đoạn giải thích ngắn, có dẫn nguồn, về việc vì sao một vùng residue được dự đoán là ATP-binding.
>
> **Quy ước nhãn:**
> - **đã kiểm (toàn văn)** = tôi đã fetch và đọc trực tiếp trang/tài liệu đó trong phiên này.
> - **đã kiểm (snippet)** = con số/khẳng định đến từ trích đoạn do công cụ tìm kiếm trả về, có gắn đúng URL nguồn, nhưng **tôi chưa đọc toàn văn** → cần xác minh lại trước khi đưa vào đề cương/luận văn.
> - **suy luận** = diễn giải hoặc tính toán của tôi, không có trong nguồn.
>
> Mốc thời gian: 01/10/2026. Một số nguồn tìm thấy là preprint 2026 chưa peer-review — đã ghi rõ.

---

## KQ1. Metric và framework đã được thiết lập cho RAG faithfulness / groundedness / attribution

### Takeaway

Không gian metric đã hội tụ về một ý tưởng chung: **phân rã câu trả lời thành claim nguyên tử, rồi kiểm tra từng claim có được passage đã truy hồi entail hay không** (RAGAS faithfulness, TruLens groundedness, FActScore, ALCE citation recall/precision, RAGChecker). Khác biệt giữa các framework nằm ở (a) ai làm trọng tài — LLM judge, NLI model nhỏ, hay người; (b) có cung cấp khoảng tin cậy thống kê hay không (chỉ ARES có). Với một sinh viên, cặp **ALCE-style citation precision/recall + RAGTruth-style span annotation** là cặp vừa rẻ vừa dễ bảo vệ nhất.

### Cited Findings

**RAGAS (Es et al., EACL 2024 demo) — công thức chính xác**

- **Faithfulness** = (số claim được context hỗ trợ) / (tổng số claim trong response); quy trình 3 bước: (1) phân rã response thành các claim nguyên tử, (2) xét từng claim có suy ra được từ retrieved context không, (3) lấy tỉ lệ. Ví dụ trong doc: câu trả lời có 2 claim, 1 được hỗ trợ → 0.5 — **đã kiểm (toàn văn)** [Ragas docs — Faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/)
- Ragas cung cấp sẵn một lựa chọn **không cần LLM judge**: **HHEM-2.1-Open của Vectara**, một classifier dựa trên T5 chuyên phát hiện hallucination, thay cho bước verify; doc gọi nó là "lightweight, open-source option for production" — **đã kiểm (toàn văn)** [Ragas docs — Faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/)
- Lưu ý vận hành: legacy metrics API của Ragas **deprecated từ v0.4, sẽ bị xoá ở v1.0**; phải dùng collections-based API — **đã kiểm (toàn văn)** [Ragas docs](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/)
- **Context Precision**: với $v_i \in \{0,1\}$ là verdict của context ở rank $i$, $P@i = \frac{\sum_{j=1}^{i} v_j}{i}$, và $AP = \frac{\sum_{i=1}^{n} P@i \cdot v_i}{\sum_{i=1}^{n} v_i + \varepsilon}$ — tức là **average precision có tính thứ tự rank** (thưởng cho việc đặt passage liên quan lên đầu) — **đã kiểm (snippet)** [Ragas metrics explained](https://saulius.io/blog/ragas-rag-evaluation-metrics-llm-judge); [Agenta — How to evaluate RAG](https://agenta.ai/blog/how-to-evaluate-rag-metrics-evals-and-best-practices)
- **Context Recall** = (số context liên quan được truy hồi) / (tổng số reference context). Cách tính thực tế: metric chạy trên **các câu của reference answer**, judge gán mỗi câu reference là *attributed* (được retrieved context hỗ trợ) hay không, điểm = trung bình các cờ attribution → **bắt buộc phải có ground-truth answer** — **đã kiểm (snippet)** [Ragas docs — Context Recall](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/)
- **Answer relevance**: tạo n câu hỏi ngược từ câu trả lời rồi đo cosine similarity với câu hỏi gốc (mô tả phổ biến trong tài liệu RAGAS) — **đã kiểm (snippet)** [Agenta](https://agenta.ai/blog/how-to-evaluate-rag-metrics-evals-and-best-practices)

**ARES (Saad-Falcon et al., NAACL 2024) — framework duy nhất có khoảng tin cậy**

- ARES sinh **LLM judge riêng cho từng component** của pipeline, là model nhẹ được fine-tune theo mục tiêu contrastive learning; báo cáo 3 điểm: **context relevance, answer faithfulness, answer relevance** — **đã kiểm (snippet)** [ARES, arXiv 2311.09476](https://arxiv.org/pdf/2311.09476); [ACL Anthology 2024.naacl-long.20](https://aclanthology.org/2024.naacl-long.20.pdf)
- Điểm khác biệt quan trọng: ARES dùng **prediction-powered inference (PPI)** để đưa ra **khoảng tin cậy thống kê** cho điểm RAG, dựa trên một tập người gán nhãn nhỏ — **khoảng 150 datapoint trở lên**, gồm cả ví dụ positive và negative cho cả ba chiều — **đã kiểm (snippet)** [ARES, arXiv 2311.09476](https://arxiv.org/pdf/2311.09476); [GitHub stanford-futuredata/ARES](https://github.com/stanford-futuredata/ARES)
- ARES tự định vị là chính xác hơn RAGAS về evaluation precision — **đã kiểm (snippet)** [ARES, arXiv 2311.09476](https://arxiv.org/pdf/2311.09476)

**TruLens RAG triad**

- Ba đánh giá: **context relevance** (mỗi chunk context có liên quan tới query), **groundedness** (tách response thành từng claim riêng rồi độc lập tìm bằng chứng hỗ trợ trong retrieved context), **answer relevance** (response có trả lời đúng input). Doc tuyên bố nếu cả ba đạt thì ứng dụng "verified to be hallucination free **up to the limit of its knowledge base**" — **đã kiểm (toàn văn)** [TruLens — RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/)
- Trang doc này **không** nêu chi tiết cơ chế tính, không nói rõ dùng LLM judge, và **không báo cáo số liệu agreement với người** — **đã kiểm (toàn văn)** [TruLens — RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/)

**AIS — Attributable to Identified Sources (Rashkin et al., Computational Linguistics 49(4), 2023; preprint 2021)** — *đây là công trình nền, cũ hơn mốc 2024–2026*

- AIS là framework yêu cầu output NLG nói về thế giới bên ngoài phải **verify được dựa trên một nguồn độc lập được cung cấp kèm** — **đã kiểm (snippet)** [Measuring Attribution in NLG Models, MIT Press CL](https://direct.mit.edu/coli/article/49/4/777/116438/Measuring-Attribution-in-Natural-Language); [arXiv 2112.12870](https://arxiv.org/html/2112.12870v2)
- **Protocol gán nhãn 2 bước** (rất đáng copy nguyên xi): (1) annotator **chưa được xem source**, trả lời "tôi có hiểu và xác định được thông tin mà output này nói hay không?" (*interpretability*); (2) **chỉ nếu** output được coi là interpretable, annotator mới được xem "attributed source" và trả lời "toàn bộ thông tin được nói ở đây có attribute được về source này không?" — **đã kiểm (snippet)** [arXiv 2112.12870](https://arxiv.org/html/2112.12870v2)
- Được validate thực nghiệm trên 3 loại task: conversational QA, summarization, table-to-text; dữ liệu nhãn công bố tại [github.com/google-research-datasets/AIS](https://github.com/google-research-datasets/AIS) — **đã kiểm (snippet)** [arXiv 2112.12870](https://arxiv.org/html/2112.12870v2)

**ALCE (Gao et al., EMNLP 2023) — citation precision & recall**

- ALCE là benchmark đầu tiên cho Automatic LLMs' Citation Evaluation; ba dataset: **ASQA, QAMPARI, ELI5**; đánh giá theo 3 chiều **fluency, correctness, citation quality** — **đã kiểm (toàn văn, qua abstract + PDF)** [arXiv 2305.14627](https://arxiv.org/abs/2305.14627); [ACL 2023.emnlp-main.398](https://aclanthology.org/2023.emnlp-main.398/)
- **Citation recall** tính per-statement, giá trị 0 hoặc 1, rồi lấy trung bình trên mọi statement của response: bằng 1 **khi và chỉ khi** statement đó có **ít nhất một citation** *và* **các citation ghép lại entail statement** — **đã kiểm (snippet)** [ALCE, OpenReview PDF](https://openreview.net/pdf?id=bxFwIn0wZ0)
- **Citation precision** phát hiện các citation **không liên quan** tới claim; cố tình **không** yêu cầu cite tập tối thiểu, và **cho phép cite dư** các passage entail thông tin tương tự — **đã kiểm (snippet)** [ALCE, OpenReview PDF](https://openreview.net/pdf?id=bxFwIn0wZ0)
- Trọng tài tự động: ALCE dùng **NLI model TRUE** để xác định passage được cite có entail nội dung sinh ra không — **đã kiểm (snippet)** [ALCE](https://aclanthology.org/2023.emnlp-main.398.pdf)
- Kết quả đầu: trên **ELI5**, kể cả model tốt nhất cũng **thiếu citation support hoàn chỉnh ở 50% số lần** — **đã kiểm (snippet)** [ALCE](https://aclanthology.org/2023.emnlp-main.398.pdf)
- Paper tuyên bố các metric tự động này có **"strong correlation with human judgements"** — **đã kiểm (toàn văn abstract)** [arXiv 2305.14627](https://arxiv.org/abs/2305.14627)

**FActScore (Min et al., EMNLP 2023)**

- Phân rã generation thành **atomic fact**, validate từng cái dựa trên một knowledge source; **FActScore = % atomic fact được gán nhãn "Supported"** — **đã kiểm (snippet)** [arXiv 2305.14251](https://arxiv.org/html/2305.14251v2); [ACL 2023.emnlp-main.741](https://aclanthology.org/2023.emnlp-main.741.pdf)
- **Inter-annotator agreement** của protocol người: **96% (InstructGPT), 90% (ChatGPT), 88% (PerplexityAI)** trên task biography — **đã kiểm (snippet)** [ACL 2023.emnlp-main.741](https://aclanthology.org/2023.emnlp-main.741.pdf)
- **Estimator tự động xấp xỉ FActScore với error rate < 2%** so với nhãn người → cho phép scale không cần công người — **đã kiểm (snippet)** [arXiv 2305.14251](https://arxiv.org/html/2305.14251v2)
- ChatGPT chỉ đạt **FActScore 58%** trên biography — **đã kiểm (snippet)** [ACL 2023.emnlp-main.741](https://aclanthology.org/2023.emnlp-main.741.pdf)

**RAGTruth (Niu et al., ACL 2024) — corpus nhãn người ở mức span**

- Gần **18.000 response** sinh tự nhiên từ nhiều LLM dùng RAG, gán nhãn tay **ở cả mức case và mức word**, kèm đánh giá **cường độ hallucination**; 3 task: QA, data-to-text, news summarization — **đã kiểm (snippet)** [ACL 2024.acl-long.585](https://aclanthology.org/2024.acl-long.585/); [arXiv 2401.00396](https://arxiv.org/pdf/2401.00396)
- Protocol: **dual + triple annotation** với taxonomy 4 lớp, đạt **>91% agreement ở mức response** — **đã kiểm (snippet)** [ACL 2024.acl-long.585](https://aclanthology.org/2024.acl-long.585.pdf)
- Kết quả then chốt cho sinh viên không có GPU to: với dữ liệu chất lượng như RAGTruth, có thể **fine-tune một LLM tương đối nhỏ** và đạt hiệu năng phát hiện hallucination **cạnh tranh với các prompt-based approach dùng GPT-4** — **đã kiểm (snippet)** [arXiv 2401.00396](https://arxiv.org/pdf/2401.00396)
- Hậu duệ nhẹ: **LettuceDetect** là framework phát hiện hallucination cho RAG huấn luyện trên RAGTruth — **đã kiểm (snippet)** [arXiv 2502.17125](https://arxiv.org/pdf/2502.17125)

**Hậu duệ 2024–2026**

- **RAGChecker (NeurIPS 2024 Datasets & Benchmarks, Amazon)**: framework chẩn đoán **mức claim**, gồm **Text-to-Claim Extractor** (phân rã text thành atomic verifiable statement) và **Claim-Entailment Checker**; chẩn đoán tách biệt lỗi retriever (incompleteness) vs lỗi generator (hallucination) — **đã kiểm (snippet)** [NeurIPS 2024 PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/27245589131d17368cccdfa990cbf16e-Paper-Datasets_and_Benchmarks_Track.pdf); [arXiv 2408.08067](https://arxiv.org/html/2408.08067v1); [GitHub amazon-science/RAGChecker](https://github.com/amazon-science/RAGChecker)
- RAGChecker báo cáo **Kendall's tau 0.62–0.75 với phán xét người**, và **scoring mức claim correlate tốt hơn đáng kể so với phương pháp holistic** — **đã kiểm (snippet, con số tau lấy từ trang thứ ba nên cần xác minh lại ở paper gốc)** [Galileo — What is RAGChecker](https://galileo.ai/blog/ragchecker-fine-grained-rag-evaluation-framework); [NeurIPS 2024 PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/27245589131d17368cccdfa990cbf16e-Paper-Datasets_and_Benchmarks_Track.pdf)
- **RAG-Zeval (2025)**: hướng evaluation end-to-end rule-guided reasoning, nhấn mạnh interpretability của bản thân evaluator — **đã kiểm (snippet)** [arXiv 2505.22430](https://arxiv.org/pdf/2505.22430)
- **MedRAGChecker (preprint 2026)**: bản claim-level verification chuyên cho **biomedical RAG** — **chưa đọc, chỉ thấy tiêu đề; cần kiểm tra vì rất gần đề tài** [arXiv 2601.06519](https://arxiv.org/pdf/2601.06519)

### Inferences

- **suy luận:** Với bài toán "giải thích một vùng residue", **context recall của RAGAS gần như không dùng được** vì nó cần *reference answer* — tức phải tự viết sẵn đoạn giải thích chuẩn cho từng residue, quá tốn công. Ngược lại **faithfulness/groundedness và ALCE citation precision/recall không cần ground-truth answer**, chỉ cần (explanation, retrieved passages) → đây là metric rẻ nhất và nên là metric chính.
- **suy luận:** Cặp "RAGAS faithfulness + ALCE citation precision/recall" đo hai thứ **khác nhau** và nên báo cáo cả hai: faithfulness hỏi *claim có được corpus hỗ trợ không*, citation precision hỏi *claim có được gán đúng citation không*. Một hệ có thể faithful 100% mà citation precision thấp (cite sai passage dù nói đúng).
- **suy luận:** Thiết kế có thể bảo vệ nhất về mặt thống kê là mượn **PPI của ARES**: tự gán nhãn ~150 item, dùng LLM judge cho phần còn lại, báo cáo **điểm kèm confidence interval**. Đây là cách duy nhất tìm được cho phép nói "faithfulness = 0.78 ± 0.06" thay vì một con số trần trụi từ judge.
- **suy luận:** HHEM-2.1-Open (T5-based) và LettuceDetect (huấn luyện trên RAGTruth) là hai công cụ **chạy được trên CPU**, cho phép có một trọng tài **không phải LLM API** làm đối chứng với LLM judge — rất phù hợp ràng buộc "không GPU, budget hạn chế".

### Gaps

- Không trích được **số liệu chính xác** về human-evaluation design của ALCE (bao nhiêu item, bao nhiêu annotator, agreement bằng bao nhiêu): WebFetch trả về PDF binary và abstract chỉ nói chung "strong correlation". **Cần đọc trực tiếp Section 4/Appendix của [ALCE PDF](https://aclanthology.org/2023.emnlp-main.398.pdf).**
- Không tìm được con số agreement giữa **RAGAS judge và người** trong paper gốc RAGAS (arXiv 2309.15217) — các trang tìm được đều là blog giải thích công thức.
- TruLens không công bố human-agreement cho RAG triad trên trang doc; không rõ có ở đâu khác.
- Chưa kiểm được **MedRAGChecker** (preprint 2026) dù rất liên quan.

---

## KQ2. Điều gì đặc thù cho đánh giá RAG **y sinh**, và các tỉ lệ hallucination/attribution đo được

### Takeaway

Y sinh có bộ benchmark QA riêng (BioASQ, PubMedQA, MIRAGE) nhưng đó là benchmark **đúng/sai câu trả lời**, không phải benchmark *giải thích có dẫn nguồn*. Phần có giá trị nhất cho đề tài này là nhóm công trình đo **tỉ lệ statement không được nguồn hỗ trợ** trong y khoa — và con số rất xấu: **50–90% response của LLM không được nguồn mà chính nó cite hỗ trợ hoàn toàn**, **~30% statement không có hỗ trợ ngay cả khi có RAG**. Quan trọng hơn cả: đã có bằng chứng trực tiếp trong **protein annotation** rằng LLM bắt chước cú pháp provenance của UniProt (ECO code, PMID) với identifier **gần như luôn sai**.

### Cited Findings

**MIRAGE / MedRAG (Xiong et al., ACL Findings 2024)**

- **MIRAGE** (Medical Information Retrieval-Augmented Generation Evaluation): **7.663 câu hỏi** từ **5 dataset QA y sinh** phổ biến; tập trung vào khả năng **zero-shot** (không demonstration) để phản ánh bối cảnh y khoa thực tế — **đã kiểm (snippet)** [arXiv 2402.13178](https://arxiv.org/html/2402.13178v1); [ACL 2024.findings-acl.372](https://aclanthology.org/2024.findings-acl.372.pdf)
- **MedRAG** toolkit: 5 corpora, 4 retriever, 6 LLM (cả general và domain-specific); thí nghiệm **>1,8 nghìn tỉ token trên 41 tổ hợp** corpus × retriever × LLM — **đã kiểm (snippet)** [arXiv 2402.13178](https://arxiv.org/html/2402.13178v1)
- MedRAG cải thiện accuracy của 6 LLM **tới 18%** so với chain-of-thought prompting; phát hiện **log-linear performance scaling** và hiệu ứng **"lost-in-the-middle"** trong medical RAG — **đã kiểm (snippet)** [arXiv 2402.13178](https://arxiv.org/html/2402.13178v1)

**PubMedQA & BioASQ**

- **PubMedQA** (Jin et al., EMNLP 2019 — *cũ, nhưng vẫn là thành phần của MIRAGE*): **1k instance chuyên gia gán nhãn, 61,2k unlabeled, 211,3k sinh tự động**; mỗi instance = (question từ title bài báo, context = abstract bỏ conclusion, long answer = conclusion, answer yes/no/maybe) — **đã kiểm (snippet)** [ACL D19-1259](https://aclanthology.org/D19-1259/); [arXiv 1909.06146](https://ar5iv.labs.arxiv.org/html/1909.06146)
- PubMedQA là dataset QA đầu tiên **yêu cầu reasoning trên nội dung định lượng** của văn bản nghiên cứu y sinh — **đã kiểm (snippet)** [ACL D19-1259](https://aclanthology.org/D19-1259.pdf)
- **BioASQ** là dataset QA y sinh có nhãn lớn nhất nhưng **<3k training instance**, phần lớn là **câu hỏi factual đơn giản** — **đã kiểm (snippet, theo so sánh của chính paper PubMedQA)** [ACL D19-1259](https://aclanthology.org/D19-1259.pdf)

**SourceCheckup (Wu et al., arXiv 2402.02008 → Nature Communications 2025) — con số attribution quan trọng nhất**

- Thiết kế: **1.200 câu hỏi y khoa sinh ra**, tổng **>40.000 statement–source pair**, đánh giá **5 LLM hàng đầu**; công bố pipeline tự động **SourceCheckup** + dataset có nhãn chuyên gia y khoa — **đã kiểm (toàn văn abstract)** [arXiv 2402.02008](https://arxiv.org/abs/2402.02008); [Nature Communications s41467-025-58551-6](https://www.nature.com/articles/s41467-025-58551-6)
- **Giữa ~50% và ~90% response của LLM không được nguồn mà chúng cung cấp hỗ trợ hoàn toàn**, và đôi khi **bị nguồn đó phản bác** — **đã kiểm (toàn văn abstract)** [arXiv 2402.02008](https://arxiv.org/abs/2402.02008)
- Với **GPT-4o có web search / RAG: ~30% statement riêng lẻ không được hỗ trợ**, và **gần một nửa response không được hỗ trợ hoàn toàn** — **đã kiểm (toàn văn abstract + snippet)** [arXiv 2402.02008](https://arxiv.org/abs/2402.02008); [Stanford HAI](https://hai.stanford.edu/news/generating-medical-errors-genai-and-erroneous-medical-references)
- **Agreement giữa verifier tự động và bác sĩ**: GPT-4 đạt **88% concordance** với bác sĩ khi validate source relevance — **đã kiểm (toàn văn abstract)** [arXiv 2402.02008](https://arxiv.org/abs/2402.02008)
- Trong một vòng kiểm tra tập trung: bác sĩ xem **110 statement–source pair** mà Source Verifier gán là *unsupported*; bác sĩ **đồng ý 95,8% (CI 91,8–98,7%)** — xác nhận **105/110** statement thực sự không được bất kỳ nguồn nào của GPT-4o (RAG) hỗ trợ — **đã kiểm (snippet)** [Nature Communications s41467-025-58551-6](https://www.nature.com/articles/s41467-025-58551-6)
- Kết luận của tác giả: **"retrieval augmentation by itself is not a silver bullet"** để làm LLM có trách nhiệm hơn về mặt factual — **đã kiểm (snippet)** [Nature Communications s41467-025-58551-6](https://www.nature.com/articles/s41467-025-58551-6)

**Almanac (Zakka et al., NEJM AI, 2024)**

- LLM framework có retrieval từ **curated medical resources**, đánh giá bởi hội đồng **8 bác sĩ board-certified + 2 health care practitioner**, trên **314 câu hỏi lâm sàng thuộc 9 chuyên khoa**, so với ChatGPT-4, Bing, Bard — **đã kiểm (snippet)** [NEJM AI, AIoa2300068](https://ai.nejm.org/doi/abs/10.1056/AIoa2300068); [PubMed 38343631](https://pubmed.ncbi.nlm.nih.gov/38343631/)
- Almanac cải thiện có ý nghĩa trên các trục **factuality, completeness, user preference, adversarial safety** — **đã kiểm (snippet)** [NEJM AI](https://ai.nejm.org/doi/abs/10.1056/AIoa2300068)

**BioRAGent (Staudinger et al., arXiv 2412.12358, demo 2024/2025)**

- Hệ RAG web tương tác cho biomedical QA: LLM làm **query expansion, snippet extraction, answer generation**, giữ **transparency qua citation link trực tiếp tới document nguồn trên PubMed** và hiển thị các query đã sinh để người dùng sửa; hỗ trợ cả response ngắn và response có **inline citation** — **đã kiểm (snippet)** [arXiv 2412.12358](https://arxiv.org/html/2412.12358v1)
- Xây trên kết quả tham gia **BioASQ 2024 challenge**, cho thấy few-shot learning với LLM dùng được trong bối cảnh professional search — **đã kiểm (snippet)** [arXiv 2412.12358](https://arxiv.org/pdf/2412.12358)
- **Lưu ý trùng tên:** có một hệ khác cũng tên BioRAGent (biomedical knowledge assistant về gene/phenotype/disease, Briefings in Bioinformatics 2025) — không cùng công trình — **đã kiểm (snippet)** [Briefings in Bioinformatics bbaf539](https://academic.oup.com/bib/article/26/5/bbaf539/8284869)

**LLM có bịa citation không, và với tỉ lệ nào (y sinh)**

- **Walters & Wilder (Scientific Reports 2023)**: **55% citation của GPT-3.5 bị bịa**, so với **18% của GPT-4** trên chủ đề đa ngành — **đã kiểm (snippet)** [PMC10484980](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10484980/)
- Nội dung y khoa do ChatGPT sinh: **47% reference bị bịa, 46% là thật nhưng không chính xác, chỉ 7% thật và chính xác**; lỗi phổ biến nhất là **PMID sai**, xuất hiện ở **93%** số bài — **đã kiểm (snippet; đây là Bhattacharyya et al. 2023 — cần xác minh con số ở toàn văn)** [ResearchGate — High Rates of Fabricated and Inaccurate References in ChatGPT-Generated Medical Content](https://www.researchgate.net/publication/370919128_High_Rates_of_Fabricated_and_Inaccurate_References_in_ChatGPT-Generated_Medical_Content); [ScienceDirect — Learning to Fake It](https://www.sciencedirect.com/science/article/pii/S2949761223000366)
- Tổng hợp: các nghiên cứu trước ước lượng **30–69% reference do LLM sinh trong ngữ cảnh y sinh là bịa** — **đã kiểm (snippet)** [arXiv 2604.03173 — Detecting and Correcting Reference Hallucinations](https://arxiv.org/pdf/2604.03173)
- **Lancet 2026 — audit 2,5 triệu bài báo y sinh** (bài đã xuất bản, không phải output LLM): tỉ lệ citation bịa **tăng hơn 12 lần**, từ ~**4/10.000 bài (2023)** lên **51,3/10.000 (Q4 2025)** và **56,9/10.000 (đầu 2026)**; **review article có tỉ lệ cao hơn 57%** so với loại bài khác — **đã kiểm (snippet)** [The Lancet, PIIS0140-6736(26)00603-3](https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(26)00603-3/fulltext); [CIDRAP](https://www.cidrap.umn.edu/anti-science/review-uncovers-rising-rate-fake-references-published-biomedical-papers)

**Đặc thù protein annotation — phát hiện quan trọng nhất cho đề tài này**

- Một nghiên cứu fine-tune **Ministral bằng QLoRA cho sequence-to-function protein annotation** đo trực tiếp hiện tượng bịa provenance kiểu UniProt: **87,0% prediction có ECO tag** (khớp tần suất 88,2% trong reference annotation), nhưng **96,9% cite ít nhất một PubMed identifier không có trong reference annotation**, và **chỉ 3,5% chia sẻ bất kỳ identifier nào** với reference — **đã kiểm (toàn văn HTML)** [arXiv 2609.24538](https://arxiv.org/html/2609.24538v1)
- Hiện tượng này **tồn tại ngay cả khi prediction hoàn toàn đúng**: trong các prediction đạt điểm 10/10 mà có citation, **80,0% vẫn cite ít nhất một identifier mà reference không có** — **đã kiểm (toàn văn HTML)** [arXiv 2609.24538](https://arxiv.org/html/2609.24538v1)
- Giải thích cơ chế của tác giả (trích): *"PubMed identifiers are arbitrary integers with no relation to the amino-acid sequence, so they cannot be inferred from the input at all; the model reproduces the **shape** of a citation, which is precisely the definition of a fabricated reference."* Khuyến nghị: **bỏ hẳn evidence tag khỏi training target**, vì literature provenance không suy ra được từ chuỗi amino acid — **đã kiểm (toàn văn HTML)** [arXiv 2609.24538](https://arxiv.org/html/2609.24538v1)
- Protocol grading của họ chống lại vấn đề này **bằng thiết kế**: strip evidence tag khi parse, và hướng dẫn grader **"ignore wording and citation style"** để citation bịa không làm phồng điểm — **đã kiểm (toàn văn HTML)** [arXiv 2609.24538](https://arxiv.org/html/2609.24538v1)
- Một preprint 2026 (**BioReason-Pro**) báo **73,6% F-max** cho GO term prediction, và **chuyên gia protein người thích annotation của nó hơn ground truth UniProt trong 79% trường hợp** — **đã kiểm (snippet); đây là preprint bioRxiv chưa peer-review, con số 79% rất mạnh nên phải đọc toàn văn trước khi trích** [bioRxiv 2026.03.19.712954](https://www.biorxiv.org/content/10.64898/2026.03.19.712954v1.full.pdf)
- Hướng agent: có công trình PSB 2026 về **LLM agent cho protein function prediction** kết hợp supervised prediction (MLP trên SwissProt), homology-based prediction, **metadata có cấu trúc từ UniProtKB**, **literature từ PubMed**, và **ontology từ GO**, với agent dùng **evidence code** (EXP, IDA, IPI, IMP, IGI, IEP, TAS, IC, HTP, HDA, HMP, HGI, HEP) — **đã kiểm (snippet; WebFetch PDF thất bại nên chưa đọc toàn văn)** [PSB 2026 — Zhapa-Camacho et al.](https://psb.stanford.edu/psb-online/proceedings/psb26/zhapa-camacho.pdf)
- Hạ tầng benchmark có sẵn cho protein function: **GO Bench** (hub benchmark cho ML-based protein functional annotation, dataset và preprocessing chuẩn hoá) và metric **CAFA5 wFmax** — **đã kiểm (snippet)** [PMC10132473](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10132473/); [bioRxiv GO Bench](https://www.biorxiv.org/content/10.1101/2022.07.19.500685.full.pdf)

### Inferences

- **suy luận — đây là lập luận mạnh nhất để biện minh RQ của đề tài:** kết quả arXiv 2609.24538 cho thấy với protein annotation, **chất lượng nội dung và chất lượng provenance là hai biến tách rời**: model có thể nói đúng về chức năng mà vẫn bịa 100% PMID. Nghĩa là một RQ dạng *"tầng RAG có làm giảm tỉ lệ citation bịa so với LLM không RAG, khi giải thích vùng ATP-binding?"* là **câu hỏi mở, đo được, và có baseline xấu đã công bố** (96,9% identifier không khớp reference). Đó chính là thứ phân biệt "chúng tôi thêm LLM" với một RQ đo lường được.
- **suy luận:** Lợi thế rất lớn của ngữ cảnh protein so với clinical QA: **ground truth tồn tại và máy đọc được**. UniProt có feature `BINDING` kèm ligand ChEBI (ATP) và ECO evidence code cho từng residue — nên có thể tự động kiểm tra **(a) citation có tồn tại thật không** (PMID resolve được qua E-utilities), **(b) giải thích có mâu thuẫn với annotation UniProt không**. Clinical RAG không có đặc quyền này.
- **suy luận:** Số 30% statement unsupported của GPT-4o+RAG và 88%/95,8% agreement giữa verifier tự động và bác sĩ (SourceCheckup) cho phép đề tài **vay thiết kế đã được validate**: automated verifier chạy toàn bộ, người chỉ xác nhận một subset các case bị gán *unsupported*. Đây là mẫu "N nhỏ nhưng credible" đã qua peer-review ở Nature Communications.
- **suy luận:** Số liệu Lancet 2026 không nói về RAG, nhưng rất hữu dụng cho phần Motivation của đề cương: nó chứng minh citation bịa đã thành vấn đề đo được ở quy mô literature, không phải lo xa.

### Gaps

- **Không tìm được** benchmark hay nghiên cứu nào đánh giá **giải thích ngôn ngữ tự nhiên có dẫn nguồn cho dự đoán ở mức residue** (binding site, active site). Đây là **khoảng trống thực sự** — vừa là cơ hội (novelty) vừa là rủi ro (không có baseline để so).
- Không trích được chi tiết human-eval design của **Almanac** (bao nhiêu câu hỏi/bác sĩ, Likert scale nào, agreement bao nhiêu) — chỉ có mô tả cấp abstract; NEJM AI là paywall.
- Không đọc được toàn văn PSB 2026 (PDF lỗi parse) và BioReason-Pro (preprint) → các con số F-max 73,6% và preference 79% **chưa được xác minh**.
- Không tìm được tỉ lệ hallucination đo được cho RAG trên **InterPro/Pfam description** cụ thể.

---

## KQ3. "LLM-as-a-judge" đáng tin đến đâu, và thiết kế human-eval tối thiểu có thể bảo vệ

### Takeaway

LLM judge **có bias hệ thống đã được đo** (position, verbosity, self-preference) và một phát hiện 2026 rất đáng lo: judge verbosity tracking length ở **r = .87** so với **.44** của người — nghĩa là judge có thể đang chấm độ dài. Thực hành có thể bảo vệ: **không dùng LLM judge làm bằng chứng duy nhất**; dùng nó để scale, nhưng calibrate trên một tập người gán nhãn (ARES gợi ý **~150 item**), báo cáo agreement bằng kappa/alpha, và dùng ngưỡng **α ≥ 0.667 là sàn, ≥ 0.80 mới gọi là đáng tin**.

### Cited Findings

**Bias của LLM judge**

- **Position bias**: lựa chọn của LLM-as-a-Judge có thể bị **đảo chỉ bằng cách đổi thứ tự** các câu trả lời candidate — **đã kiểm (snippet)** [LLMs-as-Judges survey, arXiv 2412.05579](https://arxiv.org/pdf/2412.05579)
- **Verbosity bias**: xu hướng thích response dài hơn dù không thêm nội dung — **đã kiểm (snippet)** [arXiv 2412.05579](https://arxiv.org/pdf/2412.05579); [MM-JudgeBias, arXiv 2604.18164](https://arxiv.org/pdf/2604.18164)
- **Self-preference bias**: judge chấm cao hơn cho output của chính nó — **đã kiểm (snippet)** [Self-Preference Bias in LLM-as-a-Judge, arXiv 2410.21819](https://arxiv.org/pdf/2410.21819)
- Công trình LLM-judge thời đầu báo **agreement với người cao** *đồng thời* có position, verbosity và self-enhancement bias — hai điều này không loại trừ nhau — **đã kiểm (snippet)** [arXiv 2412.05579](https://arxiv.org/pdf/2412.05579)
- Phát hiện 2026 đáng chú ý: xếp hạng của LLM judge về hành vi của một model **hội tụ với self-report của chính model đó** theo cách mà xếp hạng của người **không**; và **verbosity rating của judge track độ dài thô ở r = .87, so với r = .44 ở người** — **đã kiểm (snippet)** [arXiv 2606.09843](https://arxiv.org/pdf/2606.09843)
- Người cũng bị ảnh hưởng bởi **thứ tự trình bày** lựa chọn → position bias không phải chỉ là bệnh của máy — **đã kiểm (snippet)** [arXiv 2412.05579](https://arxiv.org/pdf/2412.05579)
- Có công trình 2026 khảo sát hệ thống **các chiến lược giảm bias** trong pipeline LLM-as-a-Judge — **đã kiểm (snippet, chưa đọc toàn văn)** [Judging the Judges, arXiv 2604.23178](https://arxiv.org/pdf/2604.23178)
- Panel nhiều judge không tự động giải quyết: có bằng chứng về **family-conditioned preference** trong panel LLM-as-Judge — **đã kiểm (snippet)** [arXiv 2609.17857](https://arxiv.org/pdf/2609.17857)

**Agreement đo được giữa trọng tài tự động và người (dùng được làm mốc)**

- **FActScore**: estimator tự động sai lệch **<2%** so với FActScore của người; IAA của người **88–96%** — **đã kiểm (snippet)** [ACL 2023.emnlp-main.741](https://aclanthology.org/2023.emnlp-main.741.pdf)
- **SourceCheckup**: GPT-4 verifier đạt **88% concordance** với bác sĩ; ở vòng kiểm tra tập trung, bác sĩ đồng ý với verifier **95,8% (91,8–98,7%)** trên **110 statement–source pair** — **đã kiểm (toàn văn abstract + snippet)** [arXiv 2402.02008](https://arxiv.org/abs/2402.02008); [Nature Communications](https://www.nature.com/articles/s41467-025-58551-6)
- **RAGChecker**: Kendall's tau **0,62–0,75** với phán xét người; claim-level correlate tốt hơn holistic — **đã kiểm (snippet, cần xác minh ở paper gốc)** [Galileo](https://galileo.ai/blog/ragchecker-fine-grained-rag-evaluation-framework)
- **RAGTruth**: **>91% agreement ở mức response** giữa các annotator người, với protocol dual + triple annotation và taxonomy 4 lớp — **đã kiểm (snippet)** [ACL 2024.acl-long.585](https://aclanthology.org/2024.acl-long.585.pdf)

**Ngưỡng agreement và chọn metric**

- **Krippendorff's alpha**: **≥ 0,667 = moderate / sàn thấp nhất còn bảo vệ được cho kết luận tạm thời**; **≥ 0,80 = strong / mức thường được yêu cầu trước khi coi dữ liệu đủ đáng tin để hành động**; 0,61–0,80 theo quy ước là "substantial" — **đã kiểm (snippet; đây là ngưỡng quy ước của Krippendorff, các trang tìm được là blog/glossary chứ không phải sách gốc)** [Encord — Krippendorff's Alpha](https://encord.com/blog/interrater-reliability-krippendorffs-alpha/); [Claru — IAA metrics](https://claru.ai/glossary/inter-annotator-agreement)
- Alpha được ưu tiên vì **tổng quát hoá cho số annotator bất kỳ, xử lý được missing data, và hỗ trợ thang nominal/ordinal/interval/ratio**; phù hợp cả khi có hơn 2 annotator và nhãn thưa — **đã kiểm (snippet)** [Encord](https://encord.com/blog/interrater-reliability-krippendorffs-alpha/); [Prodigy — Annotation Metrics](https://prodi.gy/docs/metrics)
- Chọn metric IAA phụ thuộc **loại dữ liệu, số annotator, và việc có cần chance-correction / xử lý missing data**; nhiều dataset paper báo kappa **mà không tính đến class imbalance, sample size, hay trình độ annotator** → kêu gọi minh bạch hơn trong báo cáo — **đã kiểm (snippet)** [Counting on Consensus, arXiv 2603.06865](https://arxiv.org/pdf/2603.06865)
- **ARES**: PPI cần **~150 datapoint người gán nhãn trở lên**, có cả positive và negative cho từng chiều, để tính confidence interval — **đã kiểm (snippet)** [arXiv 2311.09476](https://arxiv.org/pdf/2311.09476); [GitHub ARES](https://github.com/stanford-futuredata/ARES)

### Inferences

- **suy luận — thiết kế human-eval tối thiểu đề nghị, có chỗ dựa trong tài liệu:**
  1. **N = 150 explanation** được stratified sample (ví dụ chia theo: prediction đúng/sai, số passage truy hồi được nhiều/ít, protein trong/ngoài tập huấn luyện). Con số 150 không phải tuỳ ý — nó là mức ARES yêu cầu cho PPI, nên vừa dùng để calibrate judge vừa dùng để báo CI.
  2. **2 annotator độc lập** trên toàn bộ 150 (sinh viên + một người thứ hai; nếu xin được GVHD hoặc một bạn ngành sinh học thì mạnh hơn hẳn). Nhãn **mức claim**, không phải mức explanation — vì claim-level correlate tốt hơn với người (RAGChecker) và vì RAGTruth cho thấy nhãn span khả thi.
  3. Dùng **protocol 2 bước của AIS**: hỏi interpretability trước khi cho xem source. Đây là chi tiết nhỏ nhưng là thứ reviewer/GVHD khó bắt lỗi.
  4. Báo cáo **Cohen's kappa** (2 annotator, nhãn nominal) *và* **Krippendorff's alpha** (để so được với tài liệu); đặt mục tiêu **α ≥ 0,667**, và nói thẳng nếu không đạt.
  5. Sau khi có nhãn người: báo **agreement của LLM judge với người** (accuracy + kappa), rồi mới dùng judge chạy trên vài trăm item còn lại kèm CI theo PPI.
- **suy luận:** Để chống verbosity bias một cách rẻ: **ép độ dài explanation gần như cố định** (ví dụ 3–5 câu, 1 citation/claim). Nếu mọi explanation dài tương đương thì verbosity bias gần như bị loại bỏ bằng thiết kế — rẻ hơn mọi kỹ thuật debias.
- **suy luận:** Để chống position bias trong so sánh pairwise (ví dụ "RAG vs no-RAG, bản nào groundedness tốt hơn"): chạy **cả hai thứ tự** rồi lấy trung bình, và báo cáo tỉ lệ flip. Nếu tỉ lệ flip cao thì kết luận pairwise không đứng được — đây là một kết quả đáng báo cáo, không phải thất bại.
- **suy luận:** Để chống self-preference: **judge phải khác generator**. Nếu generator là Claude thì judge nên là GPT (hoặc ngược lại), hoặc tốt hơn là một **NLI model không phải LLM** (HHEM-2.1-Open / LettuceDetect) làm trọng tài thứ hai. Ba trọng tài (LLM-A sinh, LLM-B chấm, NLI chấm) kể một câu chuyện phương pháp luận rất chắc với chi phí gần như bằng 0 cho trọng tài thứ ba.

### Gaps

- Không tìm được paper nào nói rõ một công thức/power analysis cho **sample size** của human eval trong RAG attribution (kiểu "cần N bao nhiêu để phát hiện chênh lệch 10 điểm phần trăm"). Các con số N trong tài liệu (110 ở SourceCheckup, ~150 ở ARES, 314 ở Almanac) là **mốc thực hành**, không phải kết quả thống kê.
- Không tìm được nguồn primary (sách Krippendorff 2004) cho ngưỡng 0,667/0,80 — chỉ có blog và glossary trích lại.
- Chưa tìm được nghiên cứu nào đo bias của LLM judge **riêng trong ngữ cảnh y sinh/protein** (các bias study đều trên general chat/multimodal).

---

## KQ4. Đo được cụ thể cái gì cho một **giải thích về dự đoán ở mức residue**

### Takeaway

Năm thứ đo được, xếp theo thứ tự rẻ-và-chắc giảm dần: (1) **citation precision/recall kiểu ALCE** + **citation resolvability** (PMID có tồn tại thật?); (2) **entailment mức claim** bằng NLI; (3) **contradiction với annotation UniProt** — cái này là lợi thế riêng của ngữ cảnh protein vì ground truth máy đọc được; (4) **abstention rate** khi không truy hồi được bằng chứng; (5) **sycophancy / post-hoc rationalization check** — explanation có đổi khi prediction sai không. Mỗi cái đều có tiền lệ phương pháp trong tài liệu, nhưng **chưa ai làm cho dự đoán mức residue** → đó là chỗ đóng góp.

### Cited Findings

**(1) Citation precision / recall, và citation bịa**

- Định nghĩa dùng được nguyên xi: citation recall per-statement = 1 iff có ≥1 citation **và** citation ghép lại entail statement; citation precision phát hiện citation **không liên quan**, cho phép cite dư — **đã kiểm (snippet)** [ALCE, OpenReview](https://openreview.net/pdf?id=bxFwIn0wZ0)
- **Chỉ kiểm entailment là không đủ trong protein annotation**: model fine-tune sinh ECO tag ở 87,0% prediction nhưng **96,9% cite PMID vắng mặt trong reference**, chỉ **3,5%** trùng identifier; **80,0%** prediction điểm cao nhất vẫn cite identifier sai — **đã kiểm (toàn văn)** [arXiv 2609.24538](https://arxiv.org/html/2609.24538v1)
- Lỗi PMID sai là lỗi reference phổ biến nhất trong nội dung y khoa do ChatGPT sinh (**93% số bài**) — **đã kiểm (snippet)** [ResearchGate](https://www.researchgate.net/publication/370919128_High_Rates_of_Fabricated_and_Inaccurate_References_in_ChatGPT-Generated_Medical_Content)

**(2) Entailment mức claim**

- RAGChecker: **Text-to-Claim Extractor** + **Claim-Entailment Checker**, tách được lỗi retriever (incompleteness) khỏi lỗi generator (hallucination); scoring mức claim correlate tốt hơn holistic — **đã kiểm (snippet)** [NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/27245589131d17368cccdfa990cbf16e-Paper-Datasets_and_Benchmarks_Track.pdf)
- Ragas cho phép thay bước verify bằng **HHEM-2.1-Open** (classifier T5, open-source, cấu hình được device và batch size) — **đã kiểm (toàn văn)** [Ragas docs](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/)
- RAGTruth cho thấy có thể fine-tune LLM **nhỏ** đạt hiệu năng detect hallucination cạnh tranh với prompt-based GPT-4 — **đã kiểm (snippet)** [arXiv 2401.00396](https://arxiv.org/pdf/2401.00396)
- LettuceDetect: framework phát hiện hallucination cho RAG, huấn luyện trên RAGTruth — **đã kiểm (snippet)** [arXiv 2502.17125](https://arxiv.org/pdf/2502.17125)

**(3) Mâu thuẫn với ground truth có cấu trúc**

- SourceCheckup đo không chỉ "unsupported" mà cả trường hợp response **bị nguồn được cite phản bác** ("sometimes contradicted") — tức contradiction là một hạng mục riêng, không gộp vào unsupported — **đã kiểm (toàn văn abstract)** [arXiv 2402.02008](https://arxiv.org/abs/2402.02008)
- Hệ sinh thái protein có evidence code chuẩn (**EXP, IDA, IPI, IMP, IGI, IEP, TAS, IC, HTP, HDA, HMP, HGI, HEP**) để phân biệt bằng chứng thực nghiệm với bằng chứng suy diễn — **đã kiểm (snippet)** [PSB 2026 — Zhapa-Camacho et al.](https://psb.stanford.edu/psb-online/proceedings/psb26/zhapa-camacho.pdf)
- Benchmark/metric chuẩn hoá đã có cho protein function annotation: **GO Bench**, metric **CAFA5 wFmax** — **đã kiểm (snippet)** [PMC10132473](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10132473/)
- Khuyến nghị thẳng từ công trình protein annotation: **strip evidence tag khi grading**, và yêu cầu grader "ignore wording and citation style", để citation bịa không làm phồng điểm nội dung — **đã kiểm (toàn văn)** [arXiv 2609.24538](https://arxiv.org/html/2609.24538v1)

**(4) Abstention khi không có bằng chứng**

- Có công trình đề xuất **ba metric** đánh giá khả năng RAG **từ chối request không trả lời được**, trong đó có metric khách quan **"unanswered ratio"** = % request bị để không trả lời — **đã kiểm (snippet)** [Unanswerability Evaluation for RAG, arXiv 2412.12300](https://arxiv.org/pdf/2412.12300)
- **Abstention Accuracy**: với câu hỏi được dán nhãn unanswerable từ bằng chứng có sẵn, đo model có đúng là **không** đưa ra câu trả lời không được hỗ trợ — **đã kiểm (snippet)** [arXiv 2606.10381](https://arxiv.org/pdf/2606.10381)
- Phát hiện quan trọng cho thiết kế thí nghiệm: cần **tách "thiếu bằng chứng" khỏi "bằng chứng gây nhiễu"**; model abstain đáng tin khi bằng chứng **thiếu**, nhưng dù được prompt abstain tường minh vẫn **trả lời 41,6% câu hỏi misleading** — **đã kiểm (snippet)** [arXiv 2608.22228](https://arxiv.org/html/2608.22228)
- **RefusalBench**: đánh giá selective refusal, nhận xét rằng benchmark tĩnh về unanswerability có giới hạn; refusal được coi là đúng khi **category dự đoán khớp category ground-truth** — **đã kiểm (snippet)** [arXiv 2510.10390](https://arxiv.org/pdf/2510.10390)
- **GRACE**: model cần **đánh giá độ đủ của bằng chứng** (evidence sufficiency) để có cơ chế refusal đáng tin khi context không liên quan hoặc không đầy đủ — **đã kiểm (snippet)** [arXiv 2601.04525](https://arxiv.org/pdf/2601.04525)

**(5) Sycophancy / post-hoc rationalization check**

- **SycEval** định nghĩa protocol đo được: nếu response ban đầu **đúng**, đưa rebuttal prompt kèm bằng chứng biện minh cho đáp án **sai**; nếu response ban đầu **sai**, đưa bằng chứng biện minh đáp án **đúng**. Response đổi giữa initial và rebuttal được dán nhãn sycophantic: **progressive sycophancy** (sai → đúng) và **regressive sycophancy** (đúng → sai) — **đã kiểm (snippet)** [SycEval, arXiv 2502.08177](https://arxiv.org/html/2502.08177v4)
- Trong bối cảnh giáo dục mô phỏng: khi người dùng gợi ý đáp án **đúng**, accuracy quan sát được tăng tới **+14,7%**; khi gợi ý đáp án **sai**, accuracy giảm tới **−15%** — **đã kiểm (snippet)** [arXiv 2506.10297](https://arxiv.org/pdf/2506.10297)
- **Implicit Post-Hoc Rationalization (IPHR)** được định nghĩa và đo: model quyết đáp án trước rồi dựng reasoning để biện minh. Tỉ lệ reasoning không faithful: **Claude 3.7 Sonnet 16,3%, ChatGPT-4o 7,0%, DeepSeek R1 5,3%** — **đã kiểm (snippet)** [CoT Reasoning in the Wild Is Not Always Faithful, arXiv 2503.08679](https://arxiv.org/html/2503.08679)
- **LAQuer** (Localized Attribution Queries): hướng attribution ở mức **đoạn văn được chọn** thay vì cả response — có thể liên quan khi người dùng chỉ muốn biết nguồn của một mệnh đề cụ thể — **đã kiểm (snippet, chưa đọc toàn văn)** [arXiv 2506.01187](https://arxiv.org/pdf/2506.01187)

### Inferences

- **suy luận — bộ metric đề nghị cho tầng giải thích ATP, tất cả tính tự động được:**

  | # | Metric | Định nghĩa vận hành | Cần nhãn người? | Chỗ dựa |
  |---|---|---|---|---|
  | M1 | **Citation resolvability** | % citation trong explanation resolve được thành PMID/UniProt accession/InterPro ID **thật** (gọi E-utilities / UniProt API) **và** nằm trong tập passage đã truy hồi | Không (hoàn toàn tự động) | arXiv 2609.24538 (3,5% trùng identifier) |
  | M2 | **Citation precision / recall** | ALCE per-statement, trọng tài NLI | Không (calibrate bằng người) | ALCE |
  | M3 | **Claim-level groundedness** | Ragas faithfulness = claim được support / tổng claim, trọng tài HHEM-2.1-Open + LLM judge | Không | Ragas, RAGChecker |
  | M4 | **Contradiction rate với UniProt** | % explanation chứa claim mâu thuẫn với feature `BINDING`/ligand ATP của UniProt cho protein đó | Không (UniProt là ground truth) | SourceCheckup (contradiction là hạng mục riêng) |
  | M5 | **Abstention / unanswered ratio** | % trường hợp hệ **đúng** là từ chối giải thích khi retrieval không trả về passage liên quan; đo tách hai điều kiện: *thiếu bằng chứng* và *bằng chứng gây nhiễu* (passage về kinase khác) | Không | arXiv 2412.12300, arXiv 2608.22228 |
  | M6 | **Post-hoc rationalization check** | Lấy các residue mà predictor **sai** (false positive đã biết nhờ UniProt). Nếu explanation cho FP vẫn tự tin và vẫn "dẫn nguồn" tương tự như cho TP → bằng chứng giải thích là rationalization, không phản ánh bằng chứng | Một phần | SycEval, arXiv 2503.08679 |

- **suy luận — M6 là metric hay nhất của đề tài này.** Lý do: có thể xây tập FP/TP **miễn phí** từ chính predictor + UniProt, không cần gán nhãn gì. Rồi đo xem phân phối của M1–M4 có **khác nhau giữa TP và FP** không. Nếu groundedness/citation precision **không khác nhau** giữa TP và FP → chứng minh được bằng số rằng tầng giải thích đang biện minh bất kỳ thứ gì predictor đưa ra. Nếu **có khác** (FP có abstention rate cao hơn, citation precision thấp hơn) → tầng giải thích có **giá trị chẩn đoán**, và đó là một kết quả tích cực, đáng công bố ở mức luận văn.
- **suy luận:** M5 nên có **negative control bắt buộc**: cố tình đưa passage của một kinase khác (ví dụ truy hồi cho EGFR nhưng đưa passage về VEGFR) và đo tỉ lệ hệ vẫn sinh explanation tự tin. Con số 41,6% từ arXiv 2608.22228 cho thấy đây là failure mode thật, và nó rẻ để test.
- **suy luận:** Lấy ý "strip evidence tag khi grading" từ arXiv 2609.24538: **chấm nội dung và chấm provenance tách rời**. Nếu gộp, một explanation nói đúng sinh học nhưng cite bịa sẽ được điểm tốt — chính cái bẫy mà paper đó cảnh báo.

### Gaps

- **Không tìm được công trình nào đã làm chính xác việc này** (giải thích có dẫn nguồn cho dự đoán binding-site ở mức residue, đánh giá định lượng). Các mảnh ghép đều tồn tại riêng lẻ. Đây vừa là novelty vừa là lý do phải mô tả metric cực kỹ trong đề cương — sẽ không có baseline để so.
- Chưa tìm được nghiên cứu nào đo **sycophancy của explanation khi predictor sai** trong bất kỳ bối cảnh khoa học nào (SycEval làm trên medical QA, không phải trên giải thích dự đoán của model khác).
- Không rõ UniProt coverage cho `BINDING` + ATP trên RTK đủ dày để làm ground truth cho M4 ở quy mô vài trăm residue — **cần tự kiểm bằng một query UniProt**, chưa làm trong phiên này.

---

## KQ5. Chi phí và tính khả thi (không GPU, API hosted, budget hạn chế)

### Takeaway

Phần LLM-RAG của đề tài này **rẻ đến mức không phải là ràng buộc**: sinh + chấm vài trăm explanation nằm trong khoảng **vài USD đến ~30 USD**, kể cả khi chạy lại nhiều lần cho vài cấu hình. Ràng buộc thật là **thời gian gán nhãn của người**, không phải token. Mô hình open-weight nhỏ **đủ dùng cho vai trò trọng tài** (HHEM-2.1-Open, LettuceDetect — chạy CPU), nhưng cho vai trò **generator** thì chưa có bằng chứng trong tài liệu tôi tìm được.

### Cited Findings

**Giá API hiện tại (Anthropic, bảng cache 25/09/2026)** — **đã kiểm (toàn văn, qua tài liệu nội bộ `claude-api` skill, bảng giá first-party)**

| Model | Model ID | Input $/1M | Output $/1M |
|---|---|---|---|
| Claude Haiku 4.5 | `claude-haiku-4-5` | $1,00 | $5,00 |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | $2,00 | $10,00 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | $3,00 | $15,00 |
| Claude Opus 5.5 | `claude-opus-5-5` | $4,00 | $20,00 |
| Claude Opus 5 | `claude-opus-5` | $5,00 | $25,00 |

- **Batch API: giảm 50%** mọi rate — **đã kiểm (toàn văn, tài liệu `claude-api`)**; cũng được các trang tổng hợp xác nhận: Sonnet 4.6 từ $3/$15 về $1,50/$7,50; Haiku 4.5 từ $1/$5 về $0,50/$2,50 — **đã kiểm (snippet)** [CloudZero — Anthropic Claude API pricing](https://www.cloudzero.com/blog/anthropic-claude-api-pricing/)
- **Prompt caching: cache read $0,20/MTok** trên Opus 5.5 và Sonnet 5.5 (so với $4 và $2 giá input thường) — **đã kiểm (toàn văn, tài liệu `claude-api`)**
- OpenAI (để so sánh): **GPT-5 nano $0,050/$0,400 per 1M**, **GPT-5 mini $0,125/$1,00**; thế hệ mới hơn **GPT-5.4 mini $0,75/$4,50**, **GPT-5.4 nano $0,20/$1,25**; batch giảm một nửa, cached input giảm tới 90% — **đã kiểm (snippet; đây là trang tổng hợp của bên thứ ba, không phải trang giá chính thức của OpenAI — phải xác minh lại trước khi trích vào luận văn)** [BenchLM — OpenAI API pricing Oct 2026](https://benchlm.ai/openai/api-pricing); [pricepertoken — GPT-5 mini](https://pricepertoken.com/pricing-page/model/openai-gpt-5-mini)

**Lựa chọn open-weight / không cần GPU cho vai trò trọng tài**

- **HHEM-2.1-Open** (Vectara, T5-based) được Ragas hỗ trợ sẵn như lựa chọn "lightweight, open-source" thay cho LLM judge ở bước verify — **đã kiểm (toàn văn)** [Ragas docs](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/)
- RAGTruth cho thấy **LLM tương đối nhỏ fine-tune trên dữ liệu chất lượng** đạt hiệu năng detect hallucination cạnh tranh với prompt-based GPT-4 — **đã kiểm (snippet)** [arXiv 2401.00396](https://arxiv.org/pdf/2401.00396)
- **LettuceDetect** là framework detect hallucination cho RAG huấn luyện trên RAGTruth — **đã kiểm (snippet; chưa xác minh được yêu cầu hạ tầng cụ thể)** [arXiv 2502.17125](https://arxiv.org/pdf/2502.17125)
- **ARES** dùng judge là **model nhẹ fine-tune contrastive**, không phải frontier LLM gọi API — **đã kiểm (snippet)** [arXiv 2311.09476](https://arxiv.org/pdf/2311.09476)

### Inferences

- **suy luận — ước tính chi phí (tính toán của tôi, dựa trên bảng giá đã kiểm):** giả định 1 explanation = **~2.500 token input** (system prompt + 5 passage ~400 token/passage) và **~300 token output**.

  **Sinh 300 explanation:**
  - Haiku 4.5: 750k in × $1 + 90k out × $5 = **~$1,20**
  - Sonnet 5.5: **~$2,40**
  - Opus 5.5: **~$4,80**

  **Chấm (claim-level, giả định 6 claim/explanation → 1.800 lệnh gọi, mỗi lệnh ~2.200 token in / 120 token out):**
  - Haiku 4.5: ~$5
  - Sonnet 5.5: ~$10
  - Với **Batch API (−50%)**: còn ~$2,5 / ~$5
  - Với **prompt caching** (khối passage lặp lại giữa các claim của cùng một item, cache read $0,20/MTok): phần input gần như miễn phí → **~$2–3** cho cả vòng chấm bằng Sonnet 5.5

  **Tổng một vòng đầy-đủ (sinh + chấm 300 item): dưới $15.** Chạy **5 cấu hình** (no-RAG / RAG-top3 / RAG-top10 / RAG+rerank / RAG+abstention prompt) **vẫn dưới ~$50**, và dưới ~$25 nếu dùng Haiku + batch + caching.

- **suy luận:** Kết luận thực tế: **token cost không phải ràng buộc của đề tài này.** Cái đắt là 150 item × 2 annotator gán nhãn mức claim. Nếu mỗi item mất 4 phút → ~10 giờ/annotator. Đây là con số nên đưa vào kế hoạch 14 tuần, không phải con số USD.
- **suy luận — cái gì QUÁ ĐẮT, phải loại tường minh:**
  - ❌ **Fine-tune / instruction-tune một LLM generator** (kể cả QLoRA 7B) — không GPU. arXiv 2609.24538 làm đúng việc này và cần GPU.
  - ❌ **Huấn luyện judge riêng kiểu ARES** từ đầu — cần fine-tune. Dùng judge có sẵn + PPI thì được, vì PPI chỉ cần nhãn người.
  - ❌ **Panel nhiều bác sĩ kiểu Almanac** (8 clinician + 2 practitioner trên 314 câu) — ngoài tầm với của một sinh viên.
  - ❌ **Nhãn span mức word trên quy mô RAGTruth** (18.000 response) — cắt xuống 150 item là bắt buộc.
  - ❌ Dùng **Opus-tier cho cả generator và judge trên mọi cấu hình** thì vẫn rẻ về tiền, nhưng **tốn thời gian chờ** và không cần thiết; dùng Haiku/Sonnet + batch.
  - ⚠️ **Chạy LLM generator cục bộ (Ollama)** — máy không có GPU (xem `docs/common/resources.md`), nên về nguyên tắc chạy được model 7B lượng tử hoá trên CPU nhưng **quá chậm** cho vài trăm generation; tôi **không tìm được** bằng chứng model open-weight nhỏ đủ tốt làm generator cho explanation có dẫn nguồn trong y sinh.

### Gaps

- Giá OpenAI chỉ lấy được từ trang tổng hợp bên thứ ba; **không fetch được trang pricing chính thức của OpenAI** → con số GPT-5 mini/nano phải xác minh lại.
- Không tìm được benchmark nào so **model open-weight nhỏ vs frontier API** riêng cho task **sinh explanation có citation trong y sinh** → không thể khẳng định có hay không một model open-weight "đủ tốt" làm generator.
- Không kiểm được yêu cầu hạ tầng cụ thể (CPU-only khả thi không, latency bao nhiêu) của HHEM-2.1-Open và LettuceDetect.

---

## KQ6. Phê phán mạnh nhất với "LLM giải thích dự đoán của một model" — và thiết kế sống sót được

### Takeaway

Phê phán mà GVHD gần như chắc chắn sẽ nêu: **giải thích post-hoc bằng ngôn ngữ tự nhiên có thể *plausible* mà không *faithful*** — nó mô tả một câu chuyện hợp lý thay vì cơ chế thật khiến model dự đoán như vậy. Đây không phải lo xa triết học: đã có số liệu (16,3% unfaithful reasoning ở Claude 3.7 Sonnet) và đã có công trình riêng cho đúng trường hợp "LLM giải thích model ML khác". **Cách sống sót là đừng tuyên bố faithfulness với predictor** — hãy định nghĩa lại cái mà tầng giải thích làm là **evidence retrieval + attribution có kiểm chứng được**, và đo nó bằng ground truth bên ngoài (UniProt), chứ không bằng "nó có phản ánh đúng trọng số của CNN không".

### Cited Findings

**Phê phán cốt lõi: plausible ≠ faithful**

- Phân biệt nền tảng: **faithfulness** là mức độ explanation phản ánh đúng reasoning nội tại của model; **plausibility** chỉ là "nghe có vẻ đúng" / thuyết phục với người. Explanation **plausible nhưng unfaithful là nguy hiểm**, vì nó khiến người dùng **over-trust** model kể cả khi model có bias không mong muốn — **đã kiểm (snippet)** [Towards Faithful Model Explanation in NLP: A Survey, CL 2024](https://aclanthology.org/2024.cl-2.6.pdf); [From Plausible to Actionable, arXiv 2607.15957](https://arxiv.org/html/2607.15957v1)
- Phê phán đúng vào trường hợp của đề tài — **LLM giải thích dự đoán của một ML model khác**: xu hướng của LLM **tóm tắt hoặc bỏ sót chi tiết** (ví dụ các decision node dư) khiến explanation **bóng bẩy nhưng unfaithful** — **đã kiểm (snippet)** [Faithful or Plausible? A Counterfactual Analysis of LLM-Generated Explanations for Machine Learning Models](https://www.researchgate.net/publication/404179702_Faithful_or_Plausible_A_Counterfactual_Analysis_of_LLM-Generated_Explanations_for_Machine_Learning_Models)
- Tổng hợp bằng chứng thực nghiệm: CoT **không được dùng một cách đáng tin trong việc ra quyết định**; explanation **bỏ sót các feature có ảnh hưởng**; các biến thể prompt gây bias **làm đổi prediction mà không được rationale thừa nhận** — **đã kiểm (snippet)** [arXiv 2607.15957](https://arxiv.org/html/2607.15957v1)

**Số liệu cụ thể về unfaithful CoT**

- **Implicit Post-Hoc Rationalization (IPHR)**: model quyết đáp án trước, rồi dựng reasoning biện minh — đặc biệt với câu hỏi binary. Tỉ lệ unfaithful reasoning đo được: **Claude 3.7 Sonnet 16,3%**, **ChatGPT-4o 7,0%**, **DeepSeek R1 5,3%** — **đã kiểm (snippet)** [arXiv 2503.08679](https://arxiv.org/html/2503.08679)
- Các kiểu unfaithfulness khác được định danh: **spurious reasoning chain** (các bước nhìn mạch lạc nhưng không có liên hệ nhân quả thật với câu hỏi/đáp án) và **silent error correction** (bước trung gian có lỗi mà model "sửa" ngầm) — **đã kiểm (snippet)** [arXiv 2503.08679](https://arxiv.org/html/2503.08679)
- Nhận xét phản trực giác, quan trọng khi thiết kế metric: **CoT unfaithful vẫn có thể có ảnh hưởng nhân quả**, còn **CoT faithful hơn lại có thể không ảnh hưởng nhân quả tới đáp án cuối** → **influence và faithfulness là hai thứ khác nhau** — **đã kiểm (snippet)** [arXiv 2503.08679](https://arxiv.org/html/2503.08679)
- Có công trình 2026 lập luận **metric-based detection của unfaithfulness thất bại chính ở nơi model sai** ("two regimes of CoT unfaithfulness") — **đã kiểm (snippet; chưa đọc toàn văn)** [arXiv 2607.23458](https://arxiv.org/html/2607.23458v2)
- Lập trường mạnh: **"Chain-of-Thought Is Not Explainability"** — CoT chỉ hỗ trợ oversight **nếu** faithful, tức reasoning được nêu phải thực sự sinh ra đáp án — **đã kiểm (snippet)** [Barez et al., Oxford AIGI 2025](https://aigi.ox.ac.uk/wp-content/uploads/2025/07/Cot_Is_Not_Explainability.pdf)
- **FaithCoT-Bench**: benchmark faithfulness ở mức instance cho CoT — **đã kiểm (snippet)** [arXiv 2510.04040](https://arxiv.org/pdf/2510.04040)
- Có cả **phía bảo vệ**: một công trình 2026 lập luận "a positive case for faithfulness" — self-explanation của LLM **giúp dự đoán được hành vi của model** — **đã kiểm (snippet; chưa đọc toàn văn; nên đọc vì là phản biện cân bằng)** [arXiv 2602.02639](https://arxiv.org/pdf/2602.02639)
- Hướng khắc phục: có công trình **huấn luyện LLM để self-explanation faithful hơn** — **đã kiểm (snippet)** [arXiv 2607.21090](https://arxiv.org/pdf/2607.21090); và **đo + giảm post-hoc rationalization** trong reverse-CoT — **đã kiểm (snippet)** [arXiv 2602.14469](https://arxiv.org/pdf/2602.14469)
- Tiền đề cổ điển (cũ hơn, nhưng nên trích vì GVHD có thể biết): work về **unfaithful explanations in chain-of-thought prompting** — **đã kiểm (snippet)** [LessWrong tóm lược Turpin et al.](https://www.lesswrong.com/posts/6eKL9wDqeiELbKPDj/unfaithful-explanations-in-chain-of-thought-prompting)

### Inferences

- **suy luận — cách đóng khung (framing) để sống sót qua phê phán này, và nên viết thẳng vào đề cương:**

  > Tầng LLM-RAG **không** được tuyên bố là giải thích *vì sao model của chúng tôi* dự đoán như vậy. Nó là một tầng **truy hồi và attribution bằng chứng**: với một vùng residue được dự đoán, nó trình bày **bằng chứng độc lập đã công bố** (UniProt annotation, PubMed, mô tả Pfam/InterPro domain) **liên quan đến** vùng đó, cùng citation **kiểm chứng được**. Khẳng định được đánh giá là *"mọi claim đều truy được về một passage đã truy hồi, và không claim nào mâu thuẫn với annotation UniProt"* — **không** phải *"explanation phản ánh đúng cơ chế nội tại của predictor"*.

  Lợi thế: khẳng định này **falsifiable và đo được** (M1–M5 ở KQ4), còn khẳng định faithfulness-với-predictor thì không đo được trong khuôn khổ 14 tuần.

- **suy luận:** Nếu GVHD vẫn đẩy tới câu "nhưng nó vẫn là post-hoc rationalization": câu trả lời tốt nhất là **M6 (KQ4)** — chính đề tài **đo** hiện tượng đó. Chạy tầng giải thích trên các false positive đã biết và báo cáo xem metric groundedness/citation có phân biệt được TP khỏi FP. Như vậy phê phán bị **chuyển thành một research question**, thay vì thành một lỗ hổng. Đây là nước đi mạnh nhất về mặt chiến thuật.
- **suy luận:** Phân biệt "influence ≠ faithfulness" (arXiv 2503.08679) là lý do nên **tránh hoàn toàn các metric kiểu counterfactual/ablation trên predictor** ("nếu bỏ residue này thì explanation có đổi không") — chúng tốn kém và kết quả khó diễn giải. Giữ phạm vi ở attribution.
- **suy luận:** Nên trích cả nguồn **phản biện cân bằng** (arXiv 2602.02639, "a positive case for faithfulness") trong đề cương. Trình bày cả hai phía cho thấy sinh viên đã đọc tài liệu, chứ không chỉ đi tìm nguồn hợp ý mình.

### Gaps

- Chưa đọc toàn văn **"Faithful or Plausible? A Counterfactual Analysis of LLM-Generated Explanations for Machine Learning Models"** — đây là nguồn **khớp nhất** với tình huống của đề tài (LLM giải thích dự đoán của model ML khác) và **nên là việc đọc tiếp theo**; chỉ tìm thấy qua ResearchGate, chưa rõ venue và đã peer-review hay chưa.
- Không tìm được công trình nào bàn về faithfulness của post-hoc explanation **cho dự đoán cấu trúc/sinh học** cụ thể (binding site, structure prediction) — mọi tài liệu đều là NLP/ML tổng quát.
- Con số IPHR theo model (16,3% / 7,0% / 5,3%) lấy từ snippet; cần xác minh ở toàn văn arXiv 2503.08679 và lưu ý đây là model của **đầu 2025**, có thể đã lỗi thời so với thế hệ 2026.

---

## Ghi chú vận hành cho người viết đề cương

- **suy luận:** Ba RQ ứng viên, xếp theo độ chắc giảm dần (đều đo được trong 14 tuần, không GPU):
  1. **RQ-A (chắc nhất):** *Tầng RAG làm thay đổi citation resolvability, citation precision và contradiction-với-UniProt của explanation về vùng ATP-binding như thế nào, so với baseline LLM không RAG?* — baseline xấu đã công bố (96,9% identifier không khớp, 50–90% response không được hỗ trợ hoàn toàn), ground truth máy đọc được, hoàn toàn tự động.
  2. **RQ-B (giá trị học thuật cao nhất):** *Các metric groundedness/attribution của tầng giải thích có phân biệt được prediction đúng khỏi prediction sai của predictor?* — biến phê phán post-hoc rationalization thành kết quả.
  3. **RQ-C (bổ trợ, rẻ):** *Hệ có abstain đúng khi không có bằng chứng, và dưới bằng chứng gây nhiễu?* — chỉ cần negative control, có mốc 41,6% để so.
- **suy luận:** Mỗi RQ nên đi kèm đúng một bảng metric và một con số N. Thiếu N là chỗ GVHD sẽ hỏi đầu tiên.
- **Lưu ý quy ước repo:** đường dẫn file này (`Đề tài ATP hướng hệ thống/`) **vi phạm quy ước đặt tên trong CLAUDE.md** (chữ thường, không dấu, tiếng Anh, gạch ngang). Nếu đề tài được chốt, nên đổi thành slug kiểu `atp-binding-site-explainer/` và cập nhật mọi liên kết trỏ tới.
