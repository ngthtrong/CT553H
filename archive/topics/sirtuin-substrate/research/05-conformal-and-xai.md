# Conformal prediction và XAI cho đề tài dự đoán cơ chất SIRT1–7: bảo đảm được gì, kiểm chứng thế nào

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

Ngày: **08/10/2026**. Người soạn: Claude (agent khảo sát). Phạm vi: chỉ hai thành phần phương pháp (a) conformal prediction, (b) XAI occlusion đối chiếu motif — trong bối cảnh đề tài chính ở [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md) và [b-method-layer-draft.md](../../../surveys/b-method-layer-draft.md).

**Nhãn bằng chứng dùng trong tài liệu này:**

- `[tác giả báo cáo]` — chính tác giả bài báo nói vậy, tôi đọc được câu/định lý đó (qua toàn văn, HTML arXiv hoặc trang chính thức).
- `[tự kiểm]` — tôi tự tính, tự đối chiếu số trong phiên này.
- `[suy luận]` — tôi suy ra từ các nguồn đã dẫn; không có bài nào nói thẳng câu này.
- `[chưa kiểm]` — chỉ thấy qua tóm tắt tìm kiếm hoặc nguồn thứ cấp, **chưa đọc toàn văn**.

**Cảnh báo quan trọng ngay đầu:** mục 7 chứa một **đính chính** cho tài liệu [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md) mục 4.2: câu "Rauh báo SIRT7 ưa residue thân nước không tích điện hoặc tích điện âm ở vị trí −3, −2, +1" **có khả năng cao là gán sai isoform** (đó là phát biểu về **SIRT1**). Nếu đúng vậy thì phép kiểm XAI "có đáp án" đang dựa vào một đáp án sai. Phải mở toàn văn Rauh 2013 kiểm lại trước khi mang đi gặp GVHD.

---

## 1. Conformal prediction bảo đảm **đối tượng** nào trong bài toán đa nhãn 7 isoform?

### Takeaway

Không có một "conformal prediction" duy nhất cho bài toán đa nhãn. Có **ít nhất bốn** đối tượng khác nhau, mỗi đối tượng là một định lý khác, với giá riêng: (i) độ phủ biên cho **từng isoform tách rời** (7 bài toán nhị phân độc lập); (ii) độ phủ **có điều kiện theo lớp** (label-conditional / Mondrian) cho từng isoform; (iii) tập con isoform có bảo đảm cho **vector nhãn 7 chiều** (bài toán đa nhãn thật, không gian nhãn 2⁷ = 128); (iv) **kiểm soát rủi ro** (conformal risk control) trên một hàm mất mát như tỉ lệ bỏ sót. Đề tài phải chọn **một** và nói rõ, vì ba cái còn lại không theo sau miễn phí.

### Cited Findings

- Bảo đảm cơ bản của split/inductive conformal prediction là **độ phủ biên** (marginal coverage): với dữ liệu hiệu chỉnh và điểm test i.i.d. (hoặc trao đổi được), `1 − α ≤ P(Y_test ∈ C(X_test)) ≤ 1 − α + 1/(n+1)`. Phát biểu này là **Theorem 1 (Conformal coverage guarantee)** và **Eq. (1)** trong Angelopoulos & Bates, *A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification*; họ ghi công cho Vovk, Gammerman, Saunders. Chứng minh ở Appendix D `[tác giả báo cáo]` — [arXiv:2107.07511](https://arxiv.org/abs/2107.07511), bản HTML v6.
- Chữ "biên" (marginal) ở đây nghĩa là **lấy trung bình trên toàn bộ phân bố đầu vào**: Cauchois, Gupta & Duchi nói rõ rằng các phương pháp conformal thông thường "cho độ phủ không đều, phục vụ các ví dụ dễ và gần như bỏ qua các ví dụ khó" `[chưa kiểm — đọc qua abstract và tóm tắt]` — [JMLR 22(81), 2021](https://jmlr.csail.mit.edu/papers/v22/20-753.html) · [arXiv:2004.10181](https://arxiv.org/abs/2004.10181).
- **Độ phủ theo nhóm và theo lớp phải tự dựng, không tự có.** Angelopoulos & Bates, **Section 4.1 (Group-Balanced Conformal Prediction)**: "Để đạt độ phủ cân bằng theo nhóm, ta chỉ cần chạy conformal prediction riêng cho từng nhóm", với lượng phân vị riêng `q̂^(g)`; và họ ghi rõ conformal tiêu chuẩn "sẽ không nhất thiết cho độ phủ bên trong mỗi nhóm". Bảo đảm là **Proposition 1**. **Section 4.2 (Class-Conditional Conformal Prediction)** làm tương tự theo lớp đúng, bảo đảm là **Proposition 2** `[tác giả báo cáo]` — [arXiv:2107.07511](https://arxiv.org/abs/2107.07511).
- Họ của phương pháp hiệu chỉnh riêng theo từng "hạng mục" định trước tên là **Mondrian conformal prediction**; phân loại theo lớp (classwise) và theo cụm lớp (clustered) đều là trường hợp riêng của Mondrian `[chưa kiểm — qua tóm tắt bài Ding et al. và tài liệu dẫn lại]` — [Ding et al., NeurIPS 2023, *Class-Conditional Conformal Prediction with Many Classes*](https://arxiv.org/abs/2306.09335).
- Khái niệm "hợp lệ có điều kiện" (conditional validity) cho inductive conformal predictors được Vovk phân tích hệ thống trong *Conditional validity of inductive conformal predictors*, Machine Learning 92(2–3):349–376 (2013); bản arXiv ghi rõ inductive conformal predictors trước đó **chỉ được biết là cho độ phủ biên** `[chưa kiểm toàn văn — đọc abstract và trang xuất bản]` — [arXiv:1209.2673](https://arxiv.org/abs/1209.2673).
- **Cho đa nhãn thật**, Cauchois, Gupta & Duchi chỉ ra trở ngại cốt lõi: tập nhãn có thể lớn theo số mũ vì có `2^k` tập con nhãn; họ xử lý bằng bộ phân loại cấu trúc cây mô hình hóa tương tác giữa các nhãn `[chưa kiểm toàn văn]` — [JMLR 22(81)](https://jmlr.csail.mit.edu/papers/v22/20-753.html).
- **Lối đi thực dụng cho đa nhãn là conformal risk control**, không phải tập dự đoán. Angelopoulos & Bates **Section 4.3** lấy đúng ví dụ đa nhãn: `Y_i` là một tập con của `K` lớp, tập dự đoán `C_λ(x) = {k : f(x)_k ≥ 1 − λ}`, hàm mất mát `1 − |Y ∩ C| / |Y|` (tỉ lệ nhãn đúng bị bỏ sót), và conformal risk control tìm ngưỡng `λ̂` giữ **kỳ vọng** mất mát dưới α; bảo đảm là **Theorem 2 (Conformal Risk Control)** `[tác giả báo cáo]` — [arXiv:2107.07511](https://arxiv.org/abs/2107.07511).
- Bài gốc của kiểm soát rủi ro: Angelopoulos, Bates, Fisch, Lei, Schuster, *Conformal Risk Control*, **ICLR 2024**, [arXiv:2208.02814](https://arxiv.org/abs/2208.02814). Nó mở rộng conformal từ bảo đảm độ phủ sang **kiểm soát kỳ vọng của một hàm mất mát đơn điệu**, giữ nguyên tinh thần split conformal, và chặt tới sai số `O(1/n)`; bài còn có các mục về dịch chuyển phân bố, quantile risk control, nhiều rủi ro đồng thời `[tác giả báo cáo — qua trang kỷ yếu ICLR 2024]` — [ICLR 2024 proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html).
- Sách nền tảng của lĩnh vực: Vovk, Gammerman & Shafer, *Algorithmic Learning in a Random World* (Springer; bản 2 năm 2022) `[chưa kiểm — không mở được toàn văn trong phiên này, chỉ dẫn làm nguồn chuẩn]` — [Springer](https://link.springer.com/book/10.1007/978-3-031-06649-8).

### Inferences

- `[suy luận]` **Câu trả lời đúng cho đề tài: ba mức, phải nói rõ mức nào.**
  1. **Mức A — 7 bài toán nhị phân rời.** Với mỗi isoform `j`, dựng `C_j(x) ⊆ {0, 1}` bằng split conformal. Bảo đảm: `P(Y_j ∈ C_j(X)) ≥ 1 − α` **cho từng j, lấy trung bình trên mọi vị trí lysine**. Đây là mức dễ nhất, có định lý sạch (Theorem 1), nhưng **nói rất ít**: với mất cân bằng nặng, `C_j(x) = {0}` hầu khắp vẫn đạt độ phủ 90% mà vô dụng.
  2. **Mức B — Mondrian / label-conditional theo từng isoform.** Hiệu chỉnh riêng trên tập dương và tập âm của từng isoform: `P(Y_j ∈ C_j(X) | Y_j = 1) ≥ 1 − α`. Đây mới là thứ có nghĩa sinh học ("trong các vị trí thật là cơ chất của SIRT2, ta bắt được ≥90%"). Bảo đảm là Proposition 2 kiểu Angelopoulos & Bates, áp riêng cho mỗi isoform. **Giá: cần đủ điểm hiệu chỉnh trong lớp dương của từng isoform** — xem mục 4, và đây là chỗ SIRT1 chết.
  3. **Mức C — tập isoform có bảo đảm ("{SIRT2, SIRT3} ở mức 90%").** Đây là cách mọi bản phác trước đang **nói**, nhưng nó là một bài toán khác: nhãn đúng là một **vector 7 chiều**, nên "tập dự đoán" đúng nghĩa là một tập con của 128 vector khả dĩ, không phải một tập con của 7 isoform. Nếu muốn một phát biểu về một tập **isoform**, đối tượng đúng là **conformal risk control** trên tỉ lệ bỏ sót (Theorem 2), và phát biểu đúng phải là: *"kỳ vọng tỉ lệ isoform thật bị bỏ sót ≤ α"* — **không phải** *"xác suất tập chứa đúng toàn bộ 7 nhãn ≥ 1 − α"*.
- `[suy luận]` **Hệ quả về cách viết luận văn:** câu "conformal trả về tập isoform có bảo đảm độ phủ 90%" trong [b-method-layer-draft.md](../../../surveys/b-method-layer-draft.md) mục 3 và [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md) mục 3 là **nói quá nếu không nêu rõ đang ở mức nào**. Mức A/B bảo đảm **từng nhãn một**; muốn một phát biểu về cả 7 nhãn cùng lúc thì phải (a) hoặc chuyển sang risk control với mất mát bỏ sót, (b) hoặc hiệu chỉnh Bonferroni α/7 cho đồng thời — và lúc đó tập dự đoán phình ra.
- `[suy luận]` Nếu dùng Bonferroni cho **đồng thời 7 nhãn** ở mức α = 0,1 thì mỗi nhãn phải chạy ở α_j = 0,1/7 ≈ 0,0143, tức lượng phân vị 98,57%. Theo Table 1 (mục 4) chi phí dữ liệu hiệu chỉnh tăng mạnh. Đây là lựa chọn phải nói ra, không phải bỏ qua.

### Gaps

- Không tìm được bài nào **đặt riêng** vấn đề conformal cho đa nhãn **mất cân bằng nặng ở mức từng nhãn** kiểu PTM (mỗi nhãn 3–40% dương, một nhãn 2,6%). Cauchois et al. và conformal risk control đều có phần đa nhãn nhưng ở bối cảnh thị giác/NLP `[chưa kiểm sâu]`.
- Chưa đọc được toàn văn Cauchois et al. 2021 (chỉ abstract + tóm tắt tìm kiếm), nên **chưa xác nhận** được tên định lý/mục cho phần đa nhãn của họ. Cần mở [arXiv:2004.10181](https://arxiv.org/abs/2004.10181) và trích đúng số định lý trước khi viết vào luận văn.
- Chưa mở được toàn văn Vovk 2013 để trích đúng định nghĩa "Mondrian" và số mục. Nguồn cho từ "Mondrian" hiện chỉ là thứ cấp `[chưa kiểm]`.

---

## 2. Giả thiết của bảo đảm, và chuyện gì xảy ra khi test là in-cell MS còn calibration là in-vitro array

### Takeaway

Bảo đảm conformal đứng trên **tính trao đổi được (exchangeability)** giữa tập hiệu chỉnh và điểm test. Mảng peptide in vitro và khối phổ trong tế bào **không trao đổi được** — và không chỉ lệch ở `P(X)` mà lệch ở cả `P(Y | X)` (một peptide bị deacetyl hóa trong ống nghiệm vẫn có thể không bị trong tế bào vì khu trú, cạnh tranh, stoichiometry). Weighted conformal prediction **không cứu được trường hợp này**, vì nó chỉ xử lý **covariate shift** với `P(Y | X)` **giữ nguyên**. Kết luận trung thực: **không có bảo đảm conformal nào chuyển sang tập in-cell nếu chỉ hiệu chỉnh trên mảng.**

### Cited Findings

- Giả thiết: Theorem 1 của Angelopoulos & Bates phát biểu cho **calibration và test i.i.d.** (và tổng quát hơn là trao đổi được) `[tác giả báo cáo]` — [arXiv:2107.07511](https://arxiv.org/abs/2107.07511).
- **Covariate shift:** Angelopoulos & Bates **Section 4.5 (Covariate Shift)** định nghĩa covariate shift là **chỉ phân bố của X thay đổi, còn quan hệ giữa X và Y không đổi**; cách chữa là **weighted conformal prediction**, dùng tỉ lệ hợp lý `w(x) = dP_test/dP`, "nâng trọng số các điểm hiệu chỉnh có khả năng xuất hiện cao hơn dưới phân bố mới"; bảo đảm là **Theorem 3** `[tác giả báo cáo]` — [arXiv:2107.07511](https://arxiv.org/abs/2107.07511).
- Bài gốc: Tibshirani, Barber, Candès, Ramdas, *Conformal Prediction Under Covariate Shift*, **NeurIPS 2019**, [arXiv:1904.06019](https://arxiv.org/abs/1904.06019). Nó mở rộng conformal ra ngoài trao đổi được, cho khoảng dự đoán hợp lệ khi phân bố covariate của train và test khác nhau, **với điều kiện tỉ lệ hợp lý được biết hoặc ước lượng chính xác được từ covariate test không nhãn**; các tác giả nói phương pháp áp dụng rộng hơn, cho mọi bối cảnh thỏa mãn một khái niệm **trao đổi được có trọng số** (weighted exchangeability) `[tác giả báo cáo — qua trang NeurIPS/arXiv]` — [NeurIPS proceedings](https://papers.nips.cc/paper/8522-conformal-prediction-under-covariate-shift) · [bản PDF của tác giả](https://www.stat.berkeley.edu/~ryantibs/papers/weightedcp.pdf).
- **Giá của trọng số:** một bài sau ghi nhận việc gán trọng số lại cho các điểm hiệu chỉnh **làm giảm cỡ mẫu hữu hiệu**, nên mất một phần độ tin cậy `[chưa kiểm — qua tóm tắt tìm kiếm của một bài hậu nghiệm]` — [arXiv:2404.15018](https://arxiv.org/pdf/2404.15018).
- **Label shift:** Podkopaev & Ramdas, *Distribution-free uncertainty quantification for classification under label shift*, **UAI 2021**, PMLR 161:844–853. Họ chỉ ra label shift **làm hỏng cả định lượng bất định**, không chỉ dự đoán — "ta trước tiên lập luận rằng nó cũng làm hỏng UQ, bằng cách cho thấy sự suy giảm độ phủ và độ hiệu chỉnh"; cách chữa là gán trọng số lại cho thủ tục conformal/binning khi **có dữ liệu không nhãn từ phân bố đích**, và họ nhấn mạnh rằng thông thường các khung này **cần dữ liệu có nhãn từ đích** để cho bảo đảm, còn dưới các giả thiết hợp lý thì chỉ dữ liệu không nhãn cũng đủ `[tác giả báo cáo — qua abstract và trang PMLR]` — [PMLR v161](https://proceedings.mlr.press/v161/podkopaev21a.html) · [arXiv:2103.03323](https://arxiv.org/abs/2103.03323).
- **Bằng chứng từ chính lĩnh vực hóa tin:** Hosni, Gillet & Marchese Robinson lập luận rằng conformal regression và Venn-ABERS **kém đi khi hợp chất test lấy từ phân bố khác** với dữ liệu huấn luyện/hiệu chỉnh, và điều này đã được chứng minh qua các cách chia không ngẫu nhiên (chia theo thời gian, theo cụm, theo scaffold) `[chưa kiểm — qua tóm tắt tìm kiếm, ACS Omega 2026]`.

### Inferences

- `[suy luận]` **Khoảng cách in-vitro → in-cell không phải covariate shift.** Lý do nằm trong chính lập luận của [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md) mục 3: peptide 13 aa không có cấu trúc, không có khu trú dưới tế bào, không có cạnh tranh enzyme, không có stoichiometry. Nghĩa là **cùng một cửa sổ chuỗi X** có thể mang nhãn khác nhau ở hai miền → `P(Y | X)` đổi. Đây là **concept shift**, không phải covariate shift. Theorem 3 (weighted CP) **không áp dụng được**: nó đòi `P(Y|X)` giữ nguyên.
- `[suy luận]` Nói nhẹ hơn: ngay cả khi ai đó muốn coi đây là covariate shift, điều kiện của Tibshirani et al. là **biết hoặc ước lượng chính xác được tỉ lệ hợp lý `w(x)`**. Để ước lượng `w` ta cần một mẫu đại diện covariate từ miền in-cell. Tập in-cell hiện có là **149 vị trí phụ thuộc SIRT2**, được chọn vì chúng *đáp ứng* SIRT2 — tức mẫu đã bị **chọn theo nhãn**, không phải mẫu covariate ngẫu nhiên của miền in-cell. Dùng nó để ước lượng `w` sẽ gộp luôn hiệu ứng chọn theo nhãn vào `w`, và bảo đảm sụp.
- `[suy luận]` **Phát biểu đúng, dùng được trong luận văn:** "Conformal cho bảo đảm độ phủ `1 − α` **trên chính phân bố mảng peptide in vitro**, với dữ liệu hiệu chỉnh tách ra từ mảng và chia theo protein để chống rò rỉ. Chúng tôi **không** tuyên bố bảo đảm nào trên tập in-cell. Thay vào đó, **mức tụt độ phủ khi chuyển sang in-cell chính là một kết quả đo được của đề tài** — nó lượng hóa khoảng cách giữa hai miền."
- `[suy luận]` Đây thực ra là một **điểm mạnh** cho RQ3, không phải điểm yếu, vì nó biến conformal từ "thêm một kỹ thuật cho đẹp" thành **dụng cụ đo khoảng cách miền**. Nhưng nó chỉ mạnh nếu nói đúng: báo *độ phủ thực nghiệm* (empirical coverage) trên in-cell, và nói thẳng rằng đó là **chẩn đoán, không phải bảo đảm**.

### Gaps

- Không tìm được bài nào đưa ra bảo đảm conformal **dưới concept shift / posterior shift tổng quát** mà không cần nhãn ở miền đích. Theo hiểu biết hiện tại của lĩnh vực (Tibshirani 2019, Podkopaev & Ramdas 2021) điều này **không làm được mà không có giả thiết thêm** — nhưng tôi **chưa tìm được một bài nói thẳng "không thể"** để dẫn. Đây là lỗ hổng dẫn nguồn, cần một lượt tìm riêng về "conformal prediction under posterior/concept shift impossibility".
- Chưa mở được toàn văn Tibshirani et al. 2019 để trích đúng số định lý (Theorem 2? Theorem 3?) và định nghĩa chính thức của weighted exchangeability `[chưa kiểm]`.

---

## 3. Có bảo đảm trung thực nào trên tập in-cell được không?

### Takeaway

**Có, nhưng chỉ với một tập hiệu chỉnh in-cell có nhãn, và chỉ ở dạng có điều kiện theo lớp dương.** Vì tập in-cell hiện tại **chỉ có nhãn dương**, cái duy nhất hiệu chỉnh được là **độ phủ có điều kiện trên lớp dương** — tức "sensitivity có bảo đảm". Không thể hiệu chỉnh độ phủ biên, không thể hiệu chỉnh specificity, không thể hiệu chỉnh precision từ dữ liệu chỉ-dương.

### Cited Findings

- Cơ sở hình thức để làm việc này tồn tại: **Proposition 2, Section 4.2** của Angelopoulos & Bates — hiệu chỉnh **bên trong từng lớp đúng**, dùng các điểm hiệu chỉnh có `Y = y` để lấy lượng phân vị riêng cho lớp `y` `[tác giả báo cáo]` — [arXiv:2107.07511](https://arxiv.org/abs/2107.07511).
- Podkopaev & Ramdas nhấn mạnh đúng ranh giới: "việc áp dụng thông thường các khung đó **đòi dữ liệu có nhãn từ phân bố đích** để cho bảo đảm" `[tác giả báo cáo — qua abstract]` — [PMLR v161](https://proceedings.mlr.press/v161/podkopaev21a.html).
- Dữ liệu hiện có: **149 vị trí** in-cell HCT116, **cả 149 đều phụ thuộc SIRT2** (log2FC < 0 ở overexpression, > 0 ở knockdown) → tập **chỉ nhãn dương**; chỉ **46/149** nằm trong 6.801 vị trí của mảng `[tự kiểm — đọc lại từ topic-final-recommendation.md mục 2.2, số do phiên trước tự đo]` — nguồn gốc: [Ridgeway et al. 2025, Commun Chem, PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/).
- Nhãn âm in-cell **định nghĩa được**: vị trí **được định lượng trong cùng thí nghiệm KO/KD nhưng không đổi** là âm in-cell cho isoform đó `[tác giả báo cáo của tài liệu nội bộ — lập luận của phiên trước, chưa có bài báo nào dẫn ra]` — [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md) mục 2.3.

### Inferences

- `[suy luận]` **Ba phương án, xếp theo mức trung thực:**

| Phương án | Bảo đảm thực sự có được | Điều kiện | Nhận xét |
|---|---|---|---|
| **P1. Hiệu chỉnh trên mảng, báo cáo trên mảng** | `P(Y_j ∈ C_j(X)) ≥ 1 − α` trên phân bố mảng (Theorem 1 / Prop. 2) | Chia theo protein, tập hiệu chỉnh tách rời | **Luôn làm được.** Đây là bảo đảm duy nhất chắc chắn của đề tài |
| **P2. Hiệu chỉnh trên mảng, đo độ phủ thực nghiệm trên in-cell** | **Không có bảo đảm.** Chỉ là **chẩn đoán dịch chuyển miền** | — | Đây là nội dung thật của RQ3; phải gọi đúng tên là "empirical coverage", không gọi là "guarantee" |
| **P3. Tách một phần tập in-cell làm hiệu chỉnh** | `P(Ŷ_j = 1 | Y_j = 1)` ≥ 1 − α **trên phân bố in-cell** (độ phủ có điều kiện lớp dương) | Cần ≥ vài chục vị trí dương in-cell **giữ riêng, không dùng để chọn mô hình**, và phần test in-cell phải trao đổi được với phần hiệu chỉnh in-cell | **Làm được với SIRT2.** Đây là bảo đảm in-cell duy nhất trung thực |

- `[suy luận]` **Tập chỉ-dương làm gì với hiệu chỉnh:** nó **không** phá được P3, vì P3 chỉ cần các điểm có `Y_j = 1`. Nhưng nó **phá hoàn toàn** mọi phát biểu về độ phủ biên, về specificity và về precision trên miền in-cell: không có điểm `Y_j = 0` nào để lấy lượng phân vị. Precision 43,0% mà bài 2025 báo **không phải** một bảo đảm — nó là một ước lượng điểm trên 149 vị trí, không có khoảng tin cậy và không có mẫu âm.
- `[suy luận]` **Hệ quả cho P3 về mặt cỡ mẫu:** 149 vị trí dương, chia 50/50 thì ~75 điểm hiệu chỉnh. Theo Table 1 ở mục 4, với α = 0,1 và δ = 0,1 thì n = 102 cho sai lệch độ phủ ε = 0,05, n = 22 cho ε = 0,10. Nghĩa là với ~75 điểm ta **chỉ nói được** "độ phủ 90% ± khoảng 0,05–0,10", và chỉ cho **SIRT2**. Với 6 isoform còn lại, hiện **không có** điểm in-cell nào → **không có bảo đảm in-cell nào cho SIRT1, 3, 4, 5, 6, 7**.
- `[suy luận]` **Câu nói nên dùng với GVHD:** "Em bảo đảm độ phủ trên miền mảng peptide. Trên miền trong tế bào, em chỉ bảo đảm được *độ phủ trên lớp dương của SIRT2*, nếu thầy đồng ý em hy sinh một nửa trong 149 vị trí để làm tập hiệu chỉnh. Mọi phát biểu mạnh hơn em không có cơ sở."

### Gaps

- Chưa kiểm được liệu 149 vị trí của Ridgeway et al. có thể coi là **trao đổi được** với một tập in-cell SIRT2 khác (ví dụ từ PRIDE) hay không — nếu không thì P3 cũng chỉ bảo đảm trên chính thí nghiệm HCT116 đó, không tổng quát hóa.
- Không tìm được tài liệu phương pháp luận nào về **conformal với dữ liệu positive-unlabeled (PU)**. Nếu nhãn âm in-cell được dựng theo cách "được định lượng nhưng không đổi" thì về bản chất đây vẫn là bài toán PU, và tôi **chưa tìm được** bài nào nói conformal cần gì trong bối cảnh PU `[chưa kiểm]`. Đây là một lỗ hổng đáng tìm tiếp.

---

## 4. Cỡ mẫu hiệu chỉnh nhỏ, mất cân bằng nặng, nhãn nhiễu làm gì với conformal?

### Takeaway

Có **con số cụ thể, dẫn được**: với α = 0,1 và độ tin cậy δ = 0,1, cần **n = 22** điểm hiệu chỉnh cho sai lệch độ phủ 0,10, **n = 102** cho 0,05, **n = 2.491** cho 0,01. Với Mondrian theo lớp dương, các con số này áp cho **từng lớp dương của từng isoform**. SIRT1 với **176 vị trí dương** chỉ đủ cho mức sai lệch thô nhất. Về nhãn nhiễu: Einbinder et al. cho tin tốt có điều kiện — nhiễu **phân tán** làm conformal **bảo thủ** (phủ hơn mức cần), nhiễu **đối kháng** thì làm tập nhỏ đi và phủ thiếu.

### Cited Findings

- **Phân bố của độ phủ thực tế:** có điều kiện theo dữ liệu hiệu chỉnh, độ phủ tuân theo **Beta(n + 1 − l, l)** với `l = ⌊(n+1)α⌋` — đây là **Eq. (16)** của Angelopoulos & Bates, và họ ghi công kết quả này cho Vladimir Vovk. **Figure 11** vẽ phân bố này với α = 0,1 cho nhiều n; phân bố hội tụ về `1 − α` với tốc độ `O(n^{-1/2})`. Với **n = 1000**, độ phủ "thường nằm giữa 0,88 và 0,92", và đó là cơ sở của quy tắc kinh nghiệm **khoảng 1000 điểm hiệu chỉnh** `[tác giả báo cáo]` — [arXiv:2107.07511](https://arxiv.org/abs/2107.07511), bản HTML v6.
- **Table 1** của cùng bài cho cỡ mẫu `n(ε)` cần thiết để sai lệch độ phủ không quá ε, với δ = 0,1 và α = 0,1 `[tác giả báo cáo]`:

| ε | 0,10 | 0,05 | 0,01 | 0,005 | 0,001 |
|---|---|---|---|---|---|
| n(ε) | **22** | **102** | **2.491** | 9.812 | 244.390 |

- **Mất cân bằng và classwise conformal:** Ding et al. (NeurIPS 2023) báo rằng khoảng cách độ phủ theo lớp của classwise conformal **co lại khi số điểm hiệu chỉnh trung bình mỗi lớp tăng**, nhưng trong chế độ ít dữ liệu nó **dao động mạnh và sinh tập dự đoán rất lớn**; ngược lại conformal biên có khoảng cách độ phủ theo lớp **gần như không giảm dù thêm bao nhiêu dữ liệu hiệu chỉnh**, nên nó phủ thiếu một số lớp và phủ thừa số khác. Cách chữa của họ là **clustered conformal**: gom các lớp có phân bố điểm conformal giống nhau rồi hiệu chỉnh ở mức cụm để chung dữ liệu; thử nghiệm trên 4 bộ ảnh tới 1000 lớp `[chưa kiểm toàn văn — qua tóm tắt tìm kiếm và trang bài]` — [arXiv:2306.09335](https://arxiv.org/abs/2306.09335).
- Một hướng khác: **RC3P** (Shi et al. 2024) chỉ áp ngưỡng theo lớp cho những lớp có sai số top-k nhỏ, báo giảm **khoảng 26%** kích thước tập so với classwise CP tiêu chuẩn `[chưa kiểm]` — [arXiv:2406.06818](https://arxiv.org/abs/2406.06818).
- **Nhãn nhiễu:** Einbinder, Feldman, Bates, Angelopoulos, Gendler, Romano, *Label Noise Robustness of Conformal Prediction*, **JMLR 25 (2024)**, tiền thân arXiv 2022 tên *Conformal Prediction is Robust to Label Noise*. Kết quả chính: conformal **vẫn phủ nhãn sạch** trừ khi nhiễu được thiết kế đối kháng; cụ thể hơn, conformal và các kỹ thuật risk-control với nhãn nhiễu **đạt rủi ro bảo thủ** so với nhãn sạch **bất cứ khi nào nhiễu là "phân tán" (dispersive) và làm tăng độ biến thiên**; nhiễu đối kháng có thể **giảm** độ bất định và làm tập dự đoán quá nhỏ, phủ thiếu, và với nhiễu bị chặn cỡ họ đề xuất cách hiệu chỉnh bù. Họ cũng mở rộng sang kiểm soát một hàm mất mát tổng quát như **tỉ lệ âm giả (false negative proportion)** `[tác giả báo cáo — qua abstract JMLR và arXiv]` — [JMLR 25/23-1549](https://www.jmlr.org/papers/v25/23-1549.html) · [arXiv:2209.14295](https://arxiv.org/abs/2209.14295) · bản hội thảo [PMLR v204](https://proceedings.mlr.press/v204/feldman23a/feldman23a.pdf).

### Inferences

- `[suy luận]` **Tính cụ thể cho từng isoform.** Giả sử chia 6.801 vị trí theo protein thành train/calib/test và dành **20% cho hiệu chỉnh** (~1.360 vị trí). Số **điểm dương** trong tập hiệu chỉnh của từng isoform, xấp xỉ bằng 20% số dương toàn bộ (số dương lấy từ [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md) mục 2.1, do phiên trước tự đo):

| | SIRT1 | SIRT2 | SIRT3 | SIRT4 | SIRT5 | SIRT6 | SIRT7 |
|---|---|---|---|---|---|---|---|
| Dương toàn bộ | 176 | 1.901 | 1.844 | 1.038 | 2.614 | 1.199 | 1.692 |
| ~20% → điểm hiệu chỉnh dương | **≈35** | ≈380 | ≈369 | ≈208 | ≈523 | ≈240 | ≈338 |
| Mức ε đạt được theo Table 1 (δ=0,1; α=0,1) | chỉ **ε≈0,10** (n≥22) | ε≈0,05 | ε≈0,05 | ε≈0,05 | ε≈0,05 | ε≈0,05 | ε≈0,05 |

  `[suy luận — tính từ Table 1 và số dương tự đo của phiên trước]`. Đọc bảng này: **sáu isoform đạt được "độ phủ 90% ± 0,05"; SIRT1 chỉ đạt "90% ± 0,10"**, tức khoảng [0,80; 1,00] — gần như vô nghĩa. Và không isoform nào đạt ε = 0,01 (cần 2.491 điểm **dương** trong tập hiệu chỉnh).
- `[suy luận]` **Cỡ mẫu tối thiểu tuyệt đối:** để split conformal ở mức α cho ra tập không-tầm-thường, cần `⌈(n+1)(1−α)⌉ ≤ n`, tức `n ≥ 1/α − 1`. Với α = 0,1 → **n ≥ 9**; với α = 0,05 → **n ≥ 19**; với Bonferroni 7 nhãn ở α = 0,1 (α_j ≈ 0,0143) → **n ≥ 69 điểm dương mỗi isoform**. SIRT1 với ~35 điểm hiệu chỉnh dương **không đạt ngưỡng Bonferroni**. Đây là một lập luận định lượng, kiểm được, nên mang đi gặp GVHD.
- `[suy luận]` **Khuyến nghị kỹ thuật:** vì SIRT1 thiếu dữ liệu và SIRT1–3 được mô tả là giống nhau nhất về đặc hiệu cơ chất (xem mục 7), **clustered conformal của Ding et al.** là lựa chọn có lý *và có lý do sinh học*: gom SIRT1 với SIRT2/SIRT3 thành một cụm hiệu chỉnh. Nhưng phải nói rõ bảo đảm lúc đó là **theo cụm**, không phải theo isoform — và như thế nó mâu thuẫn một phần với chính chủ đề "đặc hiệu isoform" của đề tài. Đây là một đánh đổi thật, phải viết ra, không được để ngầm.
- `[suy luận]` **Nhãn nhiễu của mảng Rauh có thể rơi vào phía "tốt".** Nhiễu ở đây là nhiễu đo tỉ lệ tín hiệu (sai số trung vị 0,21–0,37 theo isoform, SIRT1 cao nhất 0,37 — tự đo của phiên trước), tức nhiễu **ngẫu nhiên, phân tán**, không đối kháng. Theo Einbinder et al. thì loại nhiễu này khiến conformal **bảo thủ** so với nhãn sạch — tập dự đoán to hơn cần, nhưng **không phủ thiếu**. Đây là một lập luận dùng được trong luận văn, với điều kiện nói rõ "nếu nhiễu là dispersive", và **kiểm được** bằng cách so tập dự đoán khi hiệu chỉnh trên nhãn ngưỡng cứng vs nhãn thang liên tục có trọng số sai số.

### Gaps

- Table 1 của Angelopoulos & Bates được tính cho **α = 0,1 và δ = 0,1**. Chưa tra được bảng tương ứng cho α nhỏ hơn (cần cho Bonferroni) — phải tự tính từ phân bố Beta ở Eq. (16) `[chưa làm]`.
- Chưa tìm được bài nào định lượng riêng việc **classwise conformal dưới mất cân bằng cực đoan nhị phân** (2,6% dương như SIRT1). Ding et al. làm bối cảnh nhiều lớp cân bằng hơn `[chưa kiểm sâu]`.
- Chưa đọc toàn văn Einbinder et al. để trích đúng **định nghĩa hình thức của "dispersive noise"** và số định lý. Không được viết vào luận văn trước khi làm việc đó.

---

## 5. "Conformal prediction cho dự đoán vị trí PTM" đã có ai công bố chưa?

### Takeaway

**Chưa tìm thấy.** Hai lượt tìm (web + tìm theo từ khóa PTM) **không ra bài nào** kết hợp conformal prediction với dự đoán vị trí PTM. Nhưng conformal **đã rất phổ biến trong hóa tin/QSAR** từ 2018–2019, kể cả cho hoạt tính trên 550 đích protein, nên tính mới ở đây là **"áp dụng vào một bài toán mới"**, không phải "phương pháp mới". Đây là mức tính mới yếu, cần nói đúng.

### Cited Findings

- Lượt tìm "conformal prediction post-translational modification site prediction" (08/10/2026) **không trả về bài nào** kết hợp hai thứ; kết quả toàn là dự đoán PTM thông thường (SVM đa kernel 2017, Sitetack, PTMGPT2 2024) và **không bài nào nhắc định lượng bất định hay bảo đảm conformal** `[tự kiểm — kết quả tìm kiếm của phiên này]`.
- Khớp với kết luận độc lập của phiên trước: "Không tìm thấy bài conformal cho vị trí phospho hay cơ chất kinase" `[tác giả báo cáo của tài liệu nội bộ]` — [b-method-layer-draft.md](../../../surveys/b-method-layer-draft.md) mục 6.
- **Conformal trong hóa tin thì đã dày:** Bosc et al. (J Cheminform 2019) so conformal predictors với mô hình QSAR truyền thống trên **550 đích protein người trong ChEMBL** `[chưa kiểm toàn văn]` — [J Cheminform 13:1186/s13321-018-0325-4](https://jcheminf.biomedcentral.com/track/pdf/10.1186/s13321-018-0325-4). Có cả tổng quan riêng: *Concepts and Applications of Conformal Prediction in Computational Drug Discovery* — [arXiv:1908.03569](https://arxiv.org/pdf/1908.03569).
- Svensson et al. nêu đúng điểm bán được: conformal prediction **có sẵn một định nghĩa miền áp dụng (applicability domain)** trong lòng nó, và đó là một ưu thế chính so với QSAR thường `[chưa kiểm toàn văn — qua tóm tắt]` — [bản UCL](https://discovery-pp.ucl.ac.uk/id/eprint/10060460/1/Svensson_etal_r1.pdf).
- Oršolić & Šmuc (Bioinformatics 39(8), 2023) đề xuất "dynamic applicability domain" cho ái lực gắn hợp chất–đích bằng **local conformal prediction** `[chưa kiểm toàn văn]` — [Bioinformatics btad465](https://academic.oup.com/bioinformatics/article/39/8/btad465/7245860).

### Inferences

- `[suy luận]` **Tính mới nên nói thế nào.** Không nói "lần đầu dùng conformal trong tin sinh" (sai, hóa tin dùng từ 2018). Nói được: "theo hai lượt khảo sát ngày 08/10/2026, chưa tìm thấy công trình nào áp dụng conformal prediction cho **dự đoán vị trí PTM ở mức residue**, và chưa thấy công trình nào dùng conformal như **dụng cụ đo dịch chuyển miền in-vitro → in-cell**." Phần thứ hai mới là phần đáng gọi là đóng góp.
- `[suy luận]` **Rủi ro định vị:** nếu GVHD (hoặc phản biện) biết dòng tài liệu conformal/QSAR, câu "conformal là tính mới tin học" sẽ bị hỏi lại ngay. Phòng trước bằng cách đóng khung conformal **không phải** như đóng góp phương pháp, mà như **công cụ đo** cho RQ2 (khoảng cách miền) — đúng như đã lập luận ở mục 2.
- `[suy luận]` Khẳng định "chưa ai làm" chỉ dựa trên vài lượt tìm, nên phải viết kèm điều kiện. Trước khi gặp GVHD nên tìm thêm bằng các từ khóa khác: "Venn-ABERS phosphorylation", "calibrated uncertainty PTM prediction", "prediction sets protein residue".

### Gaps

- Chưa tìm với Google Scholar hay Semantic Scholar (chỉ WebSearch + PubMed). Khẳng định "chưa có" ở mức **`[chưa kiểm sâu]`**.
- Chưa kiểm liệu có bài nào dùng conformal cho **dự đoán ở mức residue** nói chung (vị trí gắn, cấu trúc bậc hai, disorder). Nếu có thì tiền lệ phương pháp đã tồn tại và tính mới càng mỏng.

---

## 6. Kiểm chứng lời giải thích occlusion: các cách làm được chấp nhận

### Takeaway

Có một bộ dụng cụ chuẩn, chia làm ba tầng: (1) **kiểm tra lành mạnh** (sanity checks) — randomize tham số mô hình và randomize nhãn, Adebayo et al. 2018; (2) **đo độ trung thực** (faithfulness) — comprehensiveness/sufficiency của ERASER, và deletion/insertion; (3) **kiểm tra đối chứng khi xóa gây dịch chuyển phân bố** — ROAR (remove-and-retrain) của Hooker et al. **Riêng với dữ liệu chuỗi sinh học**, có thêm một bài học đặc thù: attribution trên đầu vào one-hot có **thành phần nhiễu hệ thống do gradient ngoài simplex**, và tỉ lệ "tìm lại được motif" **không so sánh được giữa các motif** nếu không hiệu chỉnh mức may rủi.

### Cited Findings

- **Sanity checks.** Adebayo et al., *Sanity Checks for Saliency Maps*, NeurIPS 2018. Hai phép kiểm: **model parameter randomization test** (so bản đồ saliency trên mô hình đã huấn luyện với mô hình **khởi tạo ngẫu nhiên, chưa huấn luyện**, cùng kiến trúc; nếu giống nhau thì phương pháp **không nhạy với tham số mô hình** và **không đạt**) và **data randomization test** (huấn luyện trên bản dữ liệu **đã trộn nhãn ngẫu nhiên**; nếu bản đồ không đổi thì phương pháp không phụ thuộc quan hệ thật giữa đầu vào và nhãn). Họ randomize theo hai cách: tất cả trọng số một lúc, và **lũy tiến từ lớp logit xuống**. Kết quả: Guided Backpropagation gần như không đổi → hành xử như một **bộ dò biên** hơn là một lời giải thích; Gradients và Grad-CAM nhìn chung đạt `[tác giả báo cáo — qua PDF/overview]` — [arXiv:1810.03292](https://arxiv.org/abs/1810.03292).
- **Comprehensiveness / sufficiency.** DeYoung et al., *ERASER: A Benchmark to Evaluate Rationalized NLP Models*, ACL 2020. **Comprehensiveness** = mức tụt tin cậy của mô hình khi **bỏ** các token được chọn làm lý giải (cao là tốt); **sufficiency** = mức đổi tin cậy khi mô hình **chỉ thấy** phần lý giải (theo quy ước gốc, thấp là tốt). ERASER tách rõ **plausibility** (khớp với lý giải của người) và **faithfulness** (trung thực với chính lập luận của mô hình), và tác giả cố ý **không đặc quyền một chỉ số nào** `[tác giả báo cáo — qua PDF và trang ACL]` — [arXiv:1911.03429](https://arxiv.org/abs/1911.03429) · [ACL 2020](https://preview.aclanthology.org/author-url/2020.acl-main.408/). **Lưu ý quy ước dấu khác nhau giữa các bài** — phải nói rõ mình dùng quy ước nào `[chưa kiểm — cảnh báo này từ nguồn thứ cấp]`.
- Một phân tích 2020 phát hiện **lý giải do người viết không nhất thiết đạt sufficiency và comprehensiveness tốt**, và biến thiên mạnh theo bộ dữ liệu và theo lớp `[chưa kiểm — qua tóm tắt]` — [arXiv:2010.04736](https://arxiv.org/pdf/2010.04736).
- **ROAR.** Hooker, Erhan, Kindermans, Kim, *A Benchmark for Interpretability Methods in Deep Neural Networks*, NeurIPS 2019. Lập luận cốt lõi: **chỉ xóa đặc trưng lúc suy luận là sai**, vì mức tụt hiệu năng có thể đến từ **dịch chuyển phân bố dữ liệu** chứ không phải từ việc mất thông tin; nên ROOAR **huấn luyện lại mô hình từ khởi tạo ngẫu nhiên trên dữ liệu đã sửa**. Quy trình: thay tỉ lệ pixel được cho là quan trọng nhất bằng một giá trị vô thông tin cố định, làm trên **cả tập train và test**. Kết quả: nhiều phương pháp hình thức cho ước lượng **kém hơn hoặc ngang với gán tầm quan trọng ngẫu nhiên**; chỉ các biến thể dựa trên ensemble vượt rõ mức ngẫu nhiên. Con số minh họa: xóa 90% đầu vào ImageNet, mạng vẫn đạt 63,53% so với 76,68% trên dữ liệu sạch `[tác giả báo cáo — qua PDF NeurIPS/arXiv]` — [arXiv:1806.10758](https://arxiv.org/abs/1806.10758).
- **Đặc thù chuỗi sinh học — nhiễu gradient ngoài simplex.** Majdandzic et al. (nhóm Koo), *Correcting gradient-based interpretations of deep neural networks for genomics*, **Genome Biology 2023**: đầu vào one-hot là biến hạng mục nằm trên một simplex chiều thấp hơn; mạng chỉ bị ràng buộc trên simplex đó nên gradient **ngoài dữ liệu có thể tùy ý**, sinh một **thành phần gradient ngẫu nhiên biểu hiện thành nhiễu trong điểm attribution**; họ báo nhiễu này **phổ biến ở nhiều DNN genomics** và đề xuất một hiệu chỉnh thống kê, cho **cải thiện đáng kể và nhất quán** chất lượng bản đồ attribution trên dữ liệu tổng hợp có motif biết trước `[tác giả báo cáo — qua PDF Genome Biology/bioRxiv]` — [Genome Biology 10.1186/s13059-023-02956-3](https://genomebiology.biomedcentral.com/counter/pdf/10.1186/s13059-023-02956-3.pdf) · [bioRxiv 2022.04.29.490102](https://www.biorxiv.org/content/10.1101/2022.04.29.490102v2).
- **Tỉ lệ tìm lại motif cần chuẩn may rủi.** Một tiền ấn phẩm 2026 (*Recovery Rates Are Not Comparable Across Transcription Factors: Chance Correction for Attribution Evaluation*) chỉ ra mức may rủi cho độ trùng motif liên tiếp là `L/(N − L + 1)`; trên 268 yếu tố phiên mã trong UniBind, mức này trải từ **0,0118 đến 0,0427**, chênh **3,6 lần** chỉ do độ dài motif và cỡ cửa sổ; với hai yếu tố thì khoảng bootstrap của **chính mức may rủi** đã không chồng nhau, nên tỉ lệ tìm lại thô **không phải đại lượng so sánh được** `[chưa kiểm — tiền ấn phẩm, chưa phản biện; đọc qua tóm tắt]` — [arXiv:2609.16271](https://arxiv.org/pdf/2609.16271).
- Một bài vị thế 2026 đánh giá lời giải thích đối chiếu motif UniBind: với **CTCF** (đối chứng dương tỉ số tín hiệu–nhiễu cao) **mọi phương pháp đều khớp hợp lý**, trung vị điểm > 0,5; nhưng với **GATA1 và MAX**, trung vị tụt về **0,2–0,4** `[chưa kiểm — tiền ấn phẩm]` — [arXiv:2606.07607](https://arxiv.org/pdf/2606.07607).
- Một bài khác báo rằng kể cả với một CNN gần như hoàn hảo, "khó mà xác định được motif nằm ở đâu chỉ dựa vào các vết điểm quan trọng", và các phương pháp **mâu thuẫn nhau nhiều, kể cả khác dấu** (dương vs âm) cho đúng các motif thật `[chưa kiểm — tiền ấn phẩm]` — [arXiv:2410.06211](https://arxiv.org/pdf/2410.06211).

### Inferences

- `[suy luận]` **Kế hoạch kiểm chứng XAI tối thiểu, bốn tầng, cho đề tài này** (tầng 1–2 là bắt buộc, không có thì phần XAI không đáng tin):

| Tầng | Phép kiểm | Dẫn nguồn | Đạt/không đạt |
|---|---|---|---|
| **1. Lành mạnh** | Occlusion trên mô hình **chưa huấn luyện** cùng kiến trúc; và trên mô hình huấn luyện với **nhãn 7 isoform đã trộn ngẫu nhiên** | Adebayo 2018, cả hai phép kiểm | Nếu bản đồ occlusion trong hai trường hợp này **tương quan cao** với bản đồ của mô hình thật → phương pháp không nói gì về mô hình, **dừng, không báo cáo motif** |
| **2. Trung thực** | Đường **deletion** (bỏ dần k vị trí điểm cao nhất, đo tụt điểm) và đường **insertion** (chỉ giữ k vị trí điểm cao nhất); báo comprehensiveness/sufficiency theo quy ước ERASER, nói rõ dấu | DeYoung 2020 | So với **đường cơ sở xóa ngẫu nhiên** và **đường xóa theo thứ tự ngược**. Nếu đường của occlusion không tách khỏi đường ngẫu nhiên → không trung thực |
| **3. Chống nhầm do dịch chuyển phân bố** | Phiên bản **ROAR**: huấn luyện lại mô hình trên dữ liệu đã che các vị trí điểm cao, so với huấn luyện lại trên dữ liệu che ngẫu nhiên cùng số vị trí | Hooker 2019 | Đây là cách duy nhất phân biệt "mất thông tin" với "đầu vào trở nên lạ". Với cửa sổ 13 aa thì việc này **rẻ**, nên không có cớ bỏ |
| **4. Đối chiếu ngoài** | Đối chiếu bản đồ occlusion với đặc hiệu đo bằng thực nghiệm (mục 7), **có hiệu chỉnh mức may rủi** | arXiv:2609.16271 | Báo cáo tỉ lệ khớp **kèm mức may rủi** `L/(N−L+1)`; với cửa sổ 13 aa và một vị trí quan tâm thì mức may rủi là 1/12 ≈ 0,083 (sau khi loại chính lysine trung tâm) `[tự kiểm — tính theo công thức của bài đó]` |

- `[suy luận]` **Che bằng gì là một quyết định phải báo cáo.** Occlusion cần một "giá trị vô thông tin". Với chuỗi protein, các lựa chọn (thay bằng alanine, thay bằng gap/padding token, thay bằng token mask của PLM, lấy trung bình trên 20 amino acid) **không tương đương** và một số trong đó tạo ra chuỗi ngoài phân bố. Bài học của Majdandzic et al. (gradient ngoài simplex) và của Hooker et al. (dịch chuyển phân bố) nói cùng một điều theo hai cách: **giá trị che tạo ra artifact**. Khuyến nghị: dùng **occlusion kiểu marginalization** (lấy trung bình điểm dự đoán trên cả 20 amino acid ở vị trí đó) chứ không phải một token duy nhất, và báo cáo cả hai để thấy mức phụ thuộc.
- `[suy luận]` Nếu dùng ESM-2 làm mô hình nền thì bản đồ occlusion đo **tác động qua cả PLM**, không chỉ qua đầu mCNN. Nghĩa là một vị trí có thể quan trọng vì nó thay đổi embedding của **cả cửa sổ**, không phải vì nó tiếp xúc enzyme. Đây là một **cách giải thích thay thế** cho mọi tín hiệu occlusion, và phải nêu trong phần giới hạn.

### Gaps

- Chưa tìm được bài nào làm kiểm chứng faithfulness **riêng cho mô hình dự đoán PTM**. Mọi phương pháp luận dẫn ở trên là từ thị giác, NLP, hoặc genomics DNA. Việc chuyển sang chuỗi protein là **`[suy luận]`**, không có tiền lệ dẫn được.
- Ba trong các nguồn genomics (arXiv:2609.16271, 2606.07607, 2410.06211) là **tiền ấn phẩm chưa phản biện**. Không nên dựa vào chúng cho phát biểu cốt lõi của luận văn; chỉ dùng làm cảnh báo phương pháp luận.

---

## 7. Motif và đặc hiệu chuỗi quanh vị trí deacetyl hóa của sirtuin: có đủ làm "đáp án" không?

### Takeaway

**Có khả năng cao là KHÔNG, và đây là phát hiện quan trọng nhất của tài liệu này.** Bằng chứng tìm được nói: (a) Rauh 2013 kết luận mỗi sirtuin có **đặc hiệu chuỗi riêng** và các tập cơ chất **chỉ chồng nhau một phần** — tức có đặc hiệu; nhưng (b) một bài 2022 nói thẳng **không thấy bằng chứng cho một motif chuỗi ưa thích nào ở SIRT7**; (c) văn liệu cũ **mâu thuẫn** về SIRT1 (một nghiên cứu nói SIRT1 **không có** đặc hiệu chuỗi); (d) SIRT1–3 được mô tả là **giống nhau nhất** về đặc hiệu cơ chất, nên khác biệt giữa chúng rất tinh tế. **Và:** câu về SIRT7 trong [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md) mục 4.2 có vẻ là **phát biểu về SIRT1 bị gán sang SIRT7**.

### Cited Findings

- **Rauh 2013 là nguồn chuẩn.** Rauh et al., *An acetylome peptide microarray reveals specificities and deacetylation substrates for all human sirtuin isoforms*, Nat Commun 4:2327 (2013), PMID **23995836** `[tự kiểm — tra PubMed trong phiên này, đúng 1 kết quả]` — [DOI 10.1038/ncomms3327](https://www.nature.com/articles/ncomms3327).
- Mảng dùng **peptide 13-mer với acetyl-lysine ở giữa**; độ dài chọn theo kết quả trước đó cho thấy **bốn residue mỗi phía của acetyl-Lys chi phối việc nhận diện sirtuin/cơ chất** `[chưa kiểm toàn văn — qua đoạn trích trong kết quả tìm kiếm]`.
- Rauh et al. kết luận: **"Sirt6 và Sirt7 ở nhân cho thấy ưa thích chồng nhau đối với một tập nhỏ peptide nhưng hoạt tính riêng biệt trên phần lớn cơ chất của chúng"**, và **"mỗi sirtuin người có đặc hiệu chuỗi riêng của nó, và các tập vị trí cơ chất deacetyl hóa của chúng chỉ chồng nhau một phần"** `[chưa kiểm toàn văn — qua đoạn trích trong kết quả tìm kiếm]`.
- **Phát biểu "residue thân nước/không tích điện" là về SIRT1, không phải SIRT7.** Một nguồn dẫn lại Rauh 2013 gán cho **Sirt1** một ưa thích rãnh thân nước, cực, tích điện dương, với **residue không tích điện ở vị trí +2, +3 và −2**. Một nghiên cứu khác về resveratrol dùng **cùng hệ mảng** báo rằng, với ức chế, **residue thân nước có vẻ ưu tiên ở phía N và residue cực/tích điện âm ở phía C** so với acetyllysine — cũng là **phát hiện về Sirt1** `[chưa kiểm — qua tóm tắt tìm kiếm mở rộng, không mở được toàn văn]` — nghiên cứu resveratrol: [Aging 10.18632/AGING.100542](https://doi.org/10.18632/AGING.100542).
- **SIRT7 có thể không có motif.** Một bài proteomics acetylome 2022 ghi rằng **không thấy bằng chứng cho một motif vị trí acetyl hóa ưa thích nào đối với SIRT7** (bài này là nghiên cứu LC-MS/MS, không phải mảng) `[chưa kiểm — qua tóm tắt tìm kiếm]` — [Sci Rep 10.1038/s41598-022-06793-5](https://www.nature.com/articles/s41598-022-06793-5).
- **Mâu thuẫn về SIRT1.** Một nghiên cứu cũ **kết luận SIRT1 không có đặc hiệu chuỗi cơ chất**, trong khi các nghiên cứu khác báo ưa thích rõ cho SIRT2 người và cho Sir2/HST2 nấm men; một tổng quan gần hơn gói lại: "dù một số sirtuin dường như thiếu đặc hiệu chuỗi, **phần lớn nghiên cứu tìm thấy sirtuin chọn lọc cơ chất có một số loại residue quanh vị trí deacetyl hóa**" `[chưa kiểm — qua tóm tắt tìm kiếm]`.
- Ngược lại, Garske & Denu (Biochemistry 2006) với thư viện **one-bead one-compound 104.907 chuỗi 5-mer** quanh một acetyl-lysine trung tâm, sắp xếp hạt tự động và đọc 39 hạt sáng nhất bằng khối phổ, kết luận **SIRT1 phân biệt được cơ chất peptide theo ngữ cảnh**, và các hit đạt hoạt tính xúc tác cao hơn tới **20 lần** so với non-hit `[chưa kiểm toàn văn — qua tóm tắt; toàn văn ở PMC2519118]` — [PMC2519118](https://pmc.ncbi.nlm.nih.gov/articles/PMC2519118).
- **SIRT2** có bằng chứng motif tương đối rõ nhất: ưa **residue thân dầu ngay cạnh lysine bị biến đổi**, và làm giàu **serine/threonine ở vị trí +3**, với cơ sở cấu trúc là tương tác thân dầu với **Phe235 và Leu239** của SIRT2 `[chưa kiểm — nguồn là một bằng phát minh Hoa Kỳ, tức nguồn THỨ CẤP và yếu; phải tìm bài báo gốc trước khi dùng]` — [US 12371817](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12371817).
- **Cơ sở cấu trúc của đặc hiệu isoform:** một tổng quan về cấu trúc sirtuin nói rãnh gắn peptide **bảo tồn về kiến trúc nhưng có đặc điểm riêng theo isoform như phân bố điện tích và chi tiết hình dạng**; một nguồn khác lập luận túi gắn peptide "nên cho phép các tiếp xúc đặc hiệu isoform". Lớp I (SIRT1–3) **chia sẻ mức tương đồng cao nhất về đặc hiệu cơ chất** `[chưa kiểm — qua tóm tắt tìm kiếm]`.

### Inferences

- `[suy luận]` **ĐÍNH CHÍNH đề nghị cho [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md) mục 4.2.** Câu hiện có — "Rauh báo SIRT7 ưa residue thân nước không tích điện hoặc tích điện âm ở vị trí −3, −2, +1; SIRT6 có túi gắn phần lớn thân dầu" — **không khớp** với bằng chứng tìm được: (i) phát biểu về residue thân nước/không tích điện xuất hiện trong văn liệu như một phát biểu về **SIRT1** (vị trí +2, +3, −2), không phải SIRT7; (ii) một bài 2022 nói SIRT7 **không có** motif ưa thích; (iii) phát biểu "túi thân dầu" trong các nguồn tìm được gắn với **SIRT2** (Phe235, Leu239), chưa xác nhận được cho SIRT6. **Phải mở toàn văn Rauh 2013 (và hình đặc hiệu chuỗi của nó) để xác nhận hoặc sửa, trước khi đưa phép kiểm XAI này vào đề cương.** Nếu đáp án sai thì phép kiểm "XAI có đáp án" trở thành phép kiểm cho đáp án giả, và GVHD có thể bắt ngay.
- `[suy luận]` **So sánh với đề tài dự phòng B cho thấy chênh lệch lớn.** Với CDK, [b-method-layer-draft.md](../../../surveys/b-method-layer-draft.md) mục 4 đã tự đo: **1.246/1.503 (83%) cửa sổ dương có P ở +1, so với 919/29.823 (3%) cửa sổ âm**. Đó là một đáp án **mạnh, định lượng, tỉ số làm giàu ~27 lần**, đúng kiểu "đối chứng dương tỉ số tín hiệu–nhiễu cao" mà bài vị thế genomics nói là trường hợp duy nhất mọi phương pháp attribution đều khớp. **Sirtuin không có gì tương đương.** Nghĩa là: **phép kiểm XAI "có đáp án" là điểm mạnh của B, không phải của A.** Nếu phần XAI là một tiêu chí đóng góp quan trọng (tiêu chí 4 của GVHD), đây là một lý lẽ thật nghiêng về B — trái với khuyến nghị hiện tại.
- `[suy luận]` **Vậy nếu motif yếu/không có thì validation XAI dựa vào gì?** Ba lối thay thế, xếp theo độ chắc:
  1. **Đối chứng dương tự dựng từ chính dữ liệu, không từ văn liệu.** Tính mức làm giàu residue theo từng vị trí (−6…+6) cho từng isoform **trực tiếp trên 6.801 vị trí của mảng**, với kiểm định và hiệu chỉnh đa so sánh. Nếu một isoform **có** vị trí làm giàu mạnh thì đó là đáp án hợp lệ **cho isoform đó**; nếu không có thì ta đã **chứng minh** rằng không có đáp án, và đó cũng là một kết quả báo cáo được. Việc này **rẻ, làm được ngay, không cần huấn luyện mô hình**, và nên làm **trước** khi hứa gì với GVHD về phần XAI.
  2. **Đối chứng tiêu cực thay cho đối chứng dương.** Kiểm xem occlusion **không** làm nổi những thứ đáng ra phải vô can: vị trí ngoài cửa sổ ±4 (Rauh nói 4 residue mỗi phía chi phối nhận diện), và các token đệm/padding.
  3. **Đối chiếu chéo giữa các isoform.** Nếu bản đồ occlusion cho SIRT1/2/3 giống nhau hơn so với với SIRT5/6/7, điều đó khớp với phát biểu "lớp I SIRT1–3 giống nhau nhất về đặc hiệu cơ chất". Đây là **một dự đoán kiểm được**, không cần motif theo vị trí.
- `[suy luận]` **Vì sao "attribution lệch motif" KHÔNG tự động là bằng chứng lời giải thích sai** — đúng như câu hỏi đặt ra, và có bốn cách giải thích thay thế, mỗi cách có một đối chứng phân biệt được:

| Giải thích thay thế | Nghĩa là gì | Đối chứng phân biệt |
|---|---|---|
| **(A) Lời giải thích sai** (phương pháp XAI không trung thực) | Bản đồ occlusion không phản ánh thứ mô hình thật dùng | **Tầng 1 + 2 ở mục 6**: nếu occlusion **không đạt** sanity check hoặc đường deletion không tách khỏi đường ngẫu nhiên → đúng là (A) |
| **(B) Mô hình dùng tín hiệu thật ngoài motif** | Mô hình học thành phần amino acid toàn cửa sổ, tính thân nước tổng, hoặc đặc trưng toàn protein qua embedding PLM | **ROAR**: che vị trí occlusion điểm cao rồi huấn luyện lại. Nếu hiệu năng **tụt mạnh hơn** che ngẫu nhiên → thông tin thật nằm ở đó, mô hình đúng, "motif" mới là cái không đầy đủ. Thêm: **thí nghiệm tước đặc trưng** — huấn luyện mô hình chỉ với motif, so với mô hình đầy đủ; nếu mô hình đầy đủ hơn hẳn thì tồn tại tín hiệu ngoài motif |
| **(C) Motif không đầy đủ hoặc sai** | Văn liệu mâu thuẫn (SIRT1), hoặc chưa có (SIRT7) | **Tự tính mức làm giàu theo vị trí trên chính 6.801 vị trí** (lối 1 ở trên) và so với motif văn liệu. Nếu dữ liệu không ủng hộ motif văn liệu → (C) |
| **(D) Mô hình học artifact của mảng peptide** | Ví dụ: học nhận ra protein nào có nhiều vị trí trong mảng, hoặc học thiên lệch lượng enzyme khác nhau theo isoform | **Chia theo protein** (bắt buộc) + kiểm xem occlusion có làm nổi các vị trí **không thay đổi giữa các isoform** không. Nếu bản đồ của 7 isoform gần như trùng nhau thì mô hình đang học "khả năng bị deacetyl hóa chung", không học đặc hiệu isoform |

  **Đối chứng quyết định** để phân biệt (A) với (B) là **ROAR có huấn luyện lại** — đây chính là lý do Hooker et al. yêu cầu huấn luyện lại thay vì chỉ xóa lúc suy luận `[tác giả báo cáo cho lý do, suy luận cho việc áp dụng]`.
- `[suy luận]` **Kiểm chứng attribution bằng bằng chứng thực nghiệm:** Rauh et al. đã xác nhận lại trên **protein nguyên** cho ba trường hợp (MDH với Sirt3; Prx1 với Sirt5; HMG-B1 với Sirt1) `[tác giả báo cáo của tài liệu nội bộ, dẫn lại Rauh]` — [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md) mục 2.4. Ba trường hợp này là **cơ hội đối chiếu attribution ở mức từng vị trí**: nếu occlusion trên các vị trí này làm nổi đúng những residue mà Rauh thấy quan trọng, đó là bằng chứng độc lập. Ngoài ra: Garske & Denu có **39 chuỗi hit** đo bằng khối phổ với hoạt tính xúc tác cao tới 20 lần — đây là **tập peptide có nhãn hoạt tính thực nghiệm, độc lập với mảng Rauh**, dùng được làm tập đối chiếu attribution cho SIRT1 (cần mở PMC2519118 lấy danh sách chuỗi). Về tiếp xúc cấu trúc: có cấu trúc tinh thể sirtuin–peptide, nên nguyên tắc có thể đối chiếu attribution với **residue tiếp xúc trong cấu trúc** — nhưng tôi **chưa xác nhận** được có cấu trúc nào cho đủ nhiều isoform, và đây là `[chưa kiểm]`.

### Gaps

- **Không mở được toàn văn Rauh 2013.** nature.com chuyển hướng qua idp.nature.com (303), europepmc trả 403, và tra PMC bằng PMID không ra bản PMC. Đây là **lỗ hổng nghiêm trọng nhất**: toàn bộ phần "XAI có đáp án" của đề tài phụ thuộc vào hình đặc hiệu chuỗi của bài này. **Việc phải làm:** sinh viên tải PDF từ máy cá nhân (hoặc dùng DOI 10.1038/ncomms3327), mở hình đặc hiệu chuỗi, và ghi lại **chính xác** phát biểu cho từng isoform.
- Không xác nhận được nguồn gốc bài báo gốc cho phát biểu motif SIRT2 (Phe235/Leu239, Ser/Thr ở +3) — nguồn duy nhất tìm được là **bằng phát minh**, không dùng được trong luận văn.
- Chưa kiểm được có cấu trúc tinh thể sirtuin–peptide nào cho **từng** isoform trong 7 isoform, và residue tiếp xúc là gì.
- Chưa tìm được bài nào tổng hợp **motif theo từng isoform cho cả 7 sirtuin** trong một bảng. Có khả năng bảng đó không tồn tại trong văn liệu, và nếu vậy thì **chính việc dựng bảng đó từ 6.801 vị trí của mảng là một đóng góp nhỏ nhưng thật** của đề tài `[suy luận]`.

---

## 8. Ba câu nên thêm vào danh sách câu hỏi cho GVHD tuần 6

`[suy luận]` — dựa trên mục 2, 4 và 7:

1. "Conformal chỉ bảo đảm độ phủ **trên miền mảng peptide**. Trên miền trong tế bào em **không có bảo đảm nào**, trừ khi hy sinh một nửa trong 149 vị trí SIRT2 làm tập hiệu chỉnh — và cũng chỉ được *độ phủ trên lớp dương của SIRT2*. Thầy thấy mức bảo đảm đó đủ để làm một RQ không, hay em nên đóng khung conformal thành **dụng cụ đo khoảng cách miền** thay vì thành một bảo đảm?"
2. "SIRT1 chỉ có 176 vị trí dương → khoảng **35 điểm hiệu chỉnh dương**. Theo bảng cỡ mẫu của Angelopoulos & Bates, mức đó chỉ cho sai lệch độ phủ ±0,10, tức khoảng [0,80; 1,00] — gần như vô nghĩa. Thầy muốn em (a) bỏ SIRT1 khỏi phần conformal, hay (b) gom SIRT1 với SIRT2/SIRT3 thành một cụm hiệu chỉnh (clustered conformal) và nói rõ bảo đảm là theo cụm chứ không theo isoform?"
3. "Phép kiểm 'XAI có đáp án' của em dựa vào motif đặc hiệu isoform. Nhưng văn liệu **mâu thuẫn** về SIRT1 và có bài nói **SIRT7 không có motif**; còn ở đề tài dự phòng (phospho theo nhóm kinase) thì CDK có đáp án rất mạnh (83% dương có P ở +1 so với 3% âm). Thầy có coi đây là một lý do thật để nghiêng về đề tài dự phòng, hay em nên **tự dựng bảng motif theo vị trí từ 6.801 vị trí của mảng** và dùng nó làm đáp án?"

---

## 9. Việc phải làm, theo thứ tự ưu tiên

`[suy luận]`

1. **Mở toàn văn Rauh 2013 và ghi lại chính xác phát biểu đặc hiệu chuỗi cho từng isoform** (mục 7 Gaps). Không làm việc này thì cả phần XAI đứng trên cát.
2. **Tự tính mức làm giàu residue theo từng vị trí (−6…+6) cho từng isoform trên 6.801 vị trí của mảng**, có kiểm định và hiệu chỉnh đa so sánh, và báo mức làm giàu kiểu "83% vs 3%" như đã làm cho CDK. Rẻ, không cần GPU, và **quyết định phần XAI có đáng làm hay không**.
3. **Sửa mục 4.2 của [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md)** sau khi làm (1) và (2).
4. **Chọn và viết rõ mức conformal (A/B/C ở mục 1)** vào đề cương, và thay mọi câu "tập isoform có bảo đảm độ phủ 90%" bằng phát biểu đúng mức đã chọn.
5. Mở toàn văn **Cauchois et al. 2021**, **Tibshirani et al. 2019**, **Einbinder et al. 2024** để lấy đúng số định lý trước khi viết vào luận văn.
6. Tìm thêm về **conformal với dữ liệu positive-unlabeled** và **conformal dưới concept shift**, hai lỗ hổng dẫn nguồn ở mục 2 và 3.

---

## 10. Nguồn (gộp)

### Conformal prediction

- Angelopoulos & Bates, *A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification* — [arXiv:2107.07511](https://arxiv.org/abs/2107.07511) (Theorem 1, Eq. 1, Eq. 16, Figure 11, Table 1, Sections 4.1/4.2/4.3/4.5/4.6, Proposition 1, Proposition 2, Theorem 2, Theorem 3)
- Vovk, Gammerman & Shafer, *Algorithmic Learning in a Random World*, Springer (bản 2, 2022) — [Springer](https://link.springer.com/book/10.1007/978-3-031-06649-8) `[chưa kiểm]`
- Vovk, *Conditional validity of inductive conformal predictors*, Machine Learning 92(2–3):349–376, 2013 — [arXiv:1209.2673](https://arxiv.org/abs/1209.2673)
- Cauchois, Gupta & Duchi, *Knowing what you know: valid and validated confidence sets in multiclass and multilabel prediction*, JMLR 22(81), 2021 — [JMLR](https://jmlr.csail.mit.edu/papers/v22/20-753.html) · [arXiv:2004.10181](https://arxiv.org/abs/2004.10181)
- Ding, Angelopoulos, Bates, Jordan, Tibshirani, *Class-Conditional Conformal Prediction with Many Classes*, NeurIPS 2023 — [arXiv:2306.09335](https://arxiv.org/abs/2306.09335)
- Shi et al., *Conformal Prediction for Class-wise Coverage via Augmented Label Rank Calibration* (RC3P), NeurIPS 2024 — [arXiv:2406.06818](https://arxiv.org/abs/2406.06818)
- Angelopoulos, Bates, Fisch, Lei, Schuster, *Conformal Risk Control*, ICLR 2024 — [arXiv:2208.02814](https://arxiv.org/abs/2208.02814) · [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html)
- Tibshirani, Barber, Candès, Ramdas, *Conformal Prediction Under Covariate Shift*, NeurIPS 2019 — [arXiv:1904.06019](https://arxiv.org/abs/1904.06019) · [NeurIPS](https://papers.nips.cc/paper/8522-conformal-prediction-under-covariate-shift)
- Podkopaev & Ramdas, *Distribution-free uncertainty quantification for classification under label shift*, UAI 2021, PMLR 161:844–853 — [PMLR](https://proceedings.mlr.press/v161/podkopaev21a.html) · [arXiv:2103.03323](https://arxiv.org/abs/2103.03323)
- Einbinder, Feldman, Bates, Angelopoulos, Gendler, Romano, *Label Noise Robustness of Conformal Prediction*, JMLR 25, 2024 — [JMLR](https://www.jmlr.org/papers/v25/23-1549.html) · [arXiv:2209.14295](https://arxiv.org/abs/2209.14295) · [PMLR v204](https://proceedings.mlr.press/v204/feldman23a/feldman23a.pdf)
- Conformal trong hóa tin: [arXiv:1908.03569](https://arxiv.org/pdf/1908.03569) (tổng quan) · [Bosc et al., J Cheminform 2019](https://jcheminf.biomedcentral.com/track/pdf/10.1186/s13321-018-0325-4) · [Oršolić & Šmuc, Bioinformatics 2023](https://academic.oup.com/bioinformatics/article/39/8/btad465/7245860) · [Svensson et al.](https://discovery-pp.ucl.ac.uk/id/eprint/10060460/1/Svensson_etal_r1.pdf)

### XAI

- Adebayo, Gilmer, Muelly, Goodfellow, Hardt, Kim, *Sanity Checks for Saliency Maps*, NeurIPS 2018 — [arXiv:1810.03292](https://arxiv.org/abs/1810.03292)
- DeYoung et al., *ERASER: A Benchmark to Evaluate Rationalized NLP Models*, ACL 2020 — [arXiv:1911.03429](https://arxiv.org/abs/1911.03429) · [ACL](https://preview.aclanthology.org/author-url/2020.acl-main.408/)
- Hooker, Erhan, Kindermans, Kim, *A Benchmark for Interpretability Methods in Deep Neural Networks* (ROAR), NeurIPS 2019 — [arXiv:1806.10758](https://arxiv.org/abs/1806.10758)
- *Evaluating and Characterizing Human Rationales*, 2020 — [arXiv:2010.04736](https://arxiv.org/pdf/2010.04736) `[chưa kiểm]`
- Majdandzic et al., *Correcting gradient-based interpretations of deep neural networks for genomics*, Genome Biology 2023 — [DOI 10.1186/s13059-023-02956-3](https://genomebiology.biomedcentral.com/counter/pdf/10.1186/s13059-023-02956-3.pdf) · [bioRxiv](https://www.biorxiv.org/content/10.1101/2022.04.29.490102v2)
- Tiền ấn phẩm chưa phản biện (chỉ dùng làm cảnh báo phương pháp luận): [arXiv:2609.16271](https://arxiv.org/pdf/2609.16271) (hiệu chỉnh may rủi cho tỉ lệ tìm lại motif) · [arXiv:2606.07607](https://arxiv.org/pdf/2606.07607) (đánh giá IML trên motif UniBind) · [arXiv:2410.06211](https://arxiv.org/pdf/2410.06211) (các phương pháp mâu thuẫn nhau, kể cả khác dấu)

### Sinh học đặc hiệu sirtuin

- Rauh et al., *An acetylome peptide microarray reveals specificities and deacetylation substrates for all human sirtuin isoforms*, Nat Commun 4:2327, 2013, PMID 23995836 — [DOI 10.1038/ncomms3327](https://www.nature.com/articles/ncomms3327) **(chưa mở được toàn văn)**
- Garske & Denu, *SIRT1 top 40 hits: use of one-bead one-compound acetyl-peptide library...*, Biochemistry 2006 — [PMC2519118](https://pmc.ncbi.nlm.nih.gov/articles/PMC2519118) `[chưa kiểm toàn văn]`
- *Quantitative proteomic analysis of the lysine acetylome reveals diverse SIRT2 substrates*, Sci Rep 2022 (nguồn cho "không có motif ở SIRT7") — [DOI 10.1038/s41598-022-06793-5](https://www.nature.com/articles/s41598-022-06793-5) `[chưa kiểm toàn văn]`
- *Sirt1 activation by resveratrol is substrate sequence-selective*, Aging 2013 — [DOI 10.18632/AGING.100542](https://doi.org/10.18632/AGING.100542) `[chưa kiểm toàn văn]`
- Ridgeway et al. 2025, Commun Chem (nguồn của 149 vị trí in-cell) — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)
