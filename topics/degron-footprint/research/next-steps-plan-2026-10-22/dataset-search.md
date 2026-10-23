# Tìm bộ dữ liệu bổ sung cho nhãn chính — khảo sát 22/10/2026

Mục đích: tìm nguồn nhãn **bổ sung** cho bộ bão hòa Zhang 2023 (91 peptide / 89 cụm cov80 / 47.847 ô), nhằm tháo nút thắt lượng nhãn mà [G2 mở rộng](../g2-extension-2026-10-18/README.md) chỉ tới.

**Phạm vi của lượt khảo sát này.** Tra qua PubMed (truy vấn ghi ở §6), tìm kiếm web, và kiểm HTTP từng endpoint dữ liệu. **Đây không phải tổng quan hệ thống**: không đăng ký truy vấn trước, không sàng hai người độc lập, không lọc theo PRISMA. Không được viết "chưa ai làm" hay "đã khảo sát đầy đủ" dựa trên lượt này. Trạng thái truy cập là `[ĐO]` tại ngày kiểm; **nội dung** từng bảng supplementary phần lớn là `[CHƯA XÁC MINH]` vì chưa tải và chưa mở file.

## 0. Nguồn lớn nhất lại nằm trong repo `[ĐO]`

Trước khi đọc phần khảo sát nguồn ngoài: phép đếm ở [sat-filter-dropoff.json](sat-filter-dropoff.json) cho thấy bộ bão hòa **đã có tại máy** còn dư nhãn chưa dùng.

| Lý do peptide bị loại khỏi benchmark G2 | Số peptide |
|---|---:|
| Giữ lại (chính là bộ 91 peptide) | **91** |
| **Loại chỉ vì `PSI(WT) > 3,0`** (ngưỡng "là degron") | **144** |
| Không đủ 10 ô đồng nghĩa để lập mốc WT ở cả hai nửa | 10 |
| Trình tự không khớp giữa CSV quét và UniProt | 2 |
| Không suy được trình tự | 1 |
| *Tổng peptide bão hòa thô* | *248* |

Nhóm 144 peptide bị loại có PSI(WT) trung vị 3,83, tối đa 5,68. Nới ngưỡng degron thêm được:

| Ngưỡng `DEGRON_PSI_MAX` | Peptide thêm | Tổng peptide |
|---:|---:|---:|
| 3,0 *(hiện hành)* | — | 91 |
| 3,5 | +50 | 141 |
| **4,0** | **+85** | **176** |
| 4,5 | +106 | 197 |
| 5,0 | +121 | 212 |

`[DIỄN GIẢI]` Ba điều rút ra. **Một,** chỉ 13/248 peptide mất vì vấn đề kỹ thuật (trình tự, mốc WT); pipeline nhãn không rò rỉ dữ liệu một cách tình cờ. **Hai,** toàn bộ phần còn lại là một **quyết định định nghĩa** — peptide nào được coi là degron — chứ không phải giới hạn của dữ liệu. **Ba,** vì nút thắt của G2 là lượng nhãn, nguồn nhãn rẻ nhất là chính quyết định đó, không phải một bộ dữ liệu mới.

`[DIỄN GIẢI]` Cảnh báo đi kèm: nới ngưỡng **đổi nghĩa nhãn**, không phải thêm dữ liệu miễn phí. Chi tiết rủi ro và thiết kế an toàn (miền đánh giá giữ nguyên, chỉ ngân sách huấn luyện đổi) ở [README §2, P0](README.md#2-thứ-tự-thí-nghiệm). Con số 249 ghi trong [báo cáo 21/10](../metadegron-analysis-2026-10-21/README.md) là từ một phép đếm khác; phép đếm ở đây ra **248** khi lấy hợp hai nửa `sat_a`/`sat_b` qua `residue_data.SAT_PAT`.

## 1. Tiêu chí chọn, theo thứ tự ưu tiên

Nhãn chính của đề tài là ΔPSI = PSI(mutant) − PSI(WT) trên peptide 28-mer gắn đầu C của GFP, hệ GPS 6 bin. Một nguồn càng gần điều kiện này càng ít phải trả giá chuyển đổi:

| Tầng | Điều kiện | Giá trị với đề tài |
|---|---|---|
| **T1** | Cùng hệ GPS, có PSI, có **đột biến điểm** trên peptide | Cộng trực tiếp vào ô ΔPSI. Chỉ cần kiểm batch/thư viện |
| **T2** | Cùng hệ GPS, có PSI, nhưng **mức tile/peptide** (không đột biến) | Giám sát yếu / tiền huấn luyện. Cần head riêng |
| **T3** | Khác hệ đo nhưng **mức residue** và endpoint là độ dồi dào/ổn định protein | Kiểm chuyển miền, kiểm chứng ngoài. Không hợp nhất thang |
| **T4** | Nhãn nhị phân motif/E3, hoặc nhãn dự đoán | Prior, truy nguồn, đối chiếu định vị. **Không** phải nhãn hồi quy |

`[DIỄN GIẢI]` Đề tài hiện đã khai thác T2 (Voutsinos, Larsen) và đã audit T4 (MetaDegron, ELM). **Tầng chưa khai thác và có giá trị cao nhất là T1** — và nó tồn tại: cùng nhóm tác giả đã công bố thêm vài bộ saturation mutagenesis trên cùng hệ GPS/PSI, ở các lớp degron khác (C-degron, N-degron).

## 2. Ứng viên T1 — cùng hệ đo, có đột biến điểm (ưu tiên cao nhất)

Cả ba nguồn dưới đây thuộc cùng dòng phương pháp GPS của nhóm Elledge / Koren / Timms, tức **cùng đại lượng PSI** với nhãn chính của đề tài. Theo PubMed:

| Nguồn | Nội dung liên quan | Trạng thái truy cập `[ĐO]` 22/10 | Đánh giá |
|---|---|---|---|
| **Koren et al. 2018, Cell 173(7):1622–1635.e14** — [DOI 10.1016/j.cell.2018.04.028](https://doi.org/10.1016/j.cell.2018.04.028), PMID 29779948, PMC6003881 | `[ĐO]` Qua bản PMC: **Table S4 = saturation mutagenesis data** (degron glycine, RxxG, EE, R-3), chấm điểm bằng PSI; **Table S7** = GPS-peptidome C-terminal 23-mer, điểm ổn định từng peptide; Table S3 = alanine scanning 5 substrate KLHDC3. Data availability nguyên văn: *"Detailed GPS and CRISPR screen data are available in Supplemental tables S1-S13"* — **không có accession GEO/SRA** | Trang Cell **403**; bản PMC **200**; **file supplementary KHÔNG tải được** (xem §2b) | **Ứng viên số 1 nhưng đang bị chặn kỹ thuật.** Cùng endpoint PSI, có đột biến điểm. Rủi ro: thư viện **23-mer đầu C**, khác 28-mer nội vùng của nhãn chính → phải xử lý như nguồn khác thư viện (P4), không trộn mù |
| **Shimshon et al. 2024, J Cell Biol 223(8)** — [DOI 10.1083/jcb.202311035](https://doi.org/10.1083/jcb.202311035), PMID 38874443, PMC11178506 | `[CHƯA XÁC MINH]` Thư viện N-terminome, theo dõi độ ổn định protein; tìm kiếm web nêu methods có N24mer saturation mutagenesis và **ΔPSI = hiệu PSI giữa WT và mutant**. Chưa mở supplementary | rupress: **403**. Bản **PMC: 200** | Ứng viên mạnh nếu bảng ΔPSI tồn tại. Cùng định nghĩa ΔPSI. Rủi ro: N-degron phụ thuộc **đầu N và protease cắt**, cơ chế khác degron nội vùng |
| **Bekturova et al. 2025, PNAS 122(33):e2501681122** — [DOI 10.1073/pnas.2501681122](https://doi.org/10.1073/pnas.2501681122), PMID 40794836, PMC12377780 | `[CHƯA XÁC MINH]` Sàng N-terminome cho con đường Cys-Arg/N-degron; abstract nêu "mutagenesis experiments" xác định đặc hiệu theo residue sau cysteine. Quy mô đột biến chưa rõ | pnas.org: **403**. Bản **PMC: 200** | Ứng viên vừa. Có thể chỉ là mutagenesis mục tiêu, không phải bão hòa diện rộng. Kiểm quy mô trước khi đầu tư |

`[DIỄN GIẢI]` **Koren 2018 Table S4 là mục tiêu cụ thể nên nhắm trước.** Lý do: đã xác nhận có bảng saturation mutagenesis chấm bằng PSI, bản PMC truy cập được, và nguồn cùng hệ đo nên không phải bắc cầu giữa hai đại lượng khác nhau — thứ đã làm cho mọi phương án T3 đắt đỏ.

`[DIỄN GIẢI]` Nhưng đừng kỳ vọng sai quy mô: Table S4 phục vụ phân tích vài lớp degron, nên số peptide bão hòa gần như chắc chắn **nhỏ hơn** 91 peptide hiện có, có thể chỉ vài chục. Giá trị của nó không nằm ở số ô mà ở **cụm protein mới và lớp degron mới** (đầu C, các motif G-end/RxxG/EE). Vì vậy cổng P2 đặt ở *số cụm cov80 mới* chứ không ở số ô.

### §2b. Thử tải Koren 2018 Table S4 — bị chặn, và giấy phép không mở `[ĐO]`

Thực hiện 22/10/2026 theo đúng thứ tự "quyền trước, dữ liệu sau" của §4. Bằng chứng và nguyên văn: [data/raw/koren-2018-probe/SOURCE.md](../../data/raw/koren-2018-probe/SOURCE.md).

- **Danh sách file đọc được:** trang PMC liệt kê **15 file** supplementary, `NIHMS967427-supplement-{1..7}.pdf` và `{8..15}.xlsx`. Có đúng **8 file xlsx** cho 8 bảng S1–S8.
- **Tải thì không được.** Mọi lần gọi HTTP tới từng `.xlsx` trả **200 nhưng body là trang chờ `Preparing to download ...`** dài 1.817 byte. Thử lại kèm cookie session và `Referer` trang bài: y như vậy. Trang chờ nạp `secure-cookie-*.js` của NCBI, tức đòi một bước bắt tay bằng JavaScript. **Không thực hiện bước đó** — đó là cơ chế chống bot có chủ đích của nhà cung cấp.
- **Giấy phép:** `oa.fcgi?id=PMC6003881` trả **404**, nghĩa là bài **không thuộc PMC Open Access Subset**. Bản PMC là author manuscript theo NIH Public Access: **đọc tự do, không có giấy phép mở để phân phối lại**; bài gốc trên Cell là all rights reserved.

`[DIỄN GIẢI]` Hai hệ quả, và hệ quả thứ hai quan trọng hơn hệ quả thứ nhất:

1. Việc tải là **vướng kỹ thuật, không phải bế tắc**: tải bằng trình duyệt thật, hoặc qua quyền ScienceDirect của ĐHCT, hoặc hỏi tác giả. Đây là việc cần một người làm bằng tay, không phải việc script làm được.
2. Dù tải được, nguồn này **không có giấy phép mở**. Dùng nội bộ để phân tích/huấn luyện thì nằm trong phạm vi học thuật thông thường và `data/` đã gitignore; nhưng **không** được đưa bảng gốc lên git, vào phụ lục luận văn, hay vào nguyên mẫu công khai. Nếu định để nguyên mẫu công khai dùng mô hình học từ nguồn này thì phải hỏi lại quyền, không suy từ việc bài báo đọc được.

`[ĐO]` **Cập nhật sau khi tải tay (22/10):** đã mở file — Table S4 đúng là `supplement-11` (9 substrate, 3 bin, PSI ∈ [1;3]). Kết quả audit: PSI tái tính khớp, chiều ΔPSI đúng, nhưng **chỉ 5 cụm cov80 mới → cổng P2 không đạt**; vai trò còn lại là tập kiểm chứng ngoài. Chi tiết: [koren-s4-audit-2026-10-22](../koren-s4-audit-2026-10-22/README.md).

### Ứng viên T1 chưa xác minh, cần tra tiếp

- `[ĐO]` **Timms et al. 2023, Mol Cell** — C-degron không phụ thuộc ubiquitin, [DOI 10.1016/j.molcel.2023.04.023](https://doi.org/10.1016/j.molcel.2023.04.023), PMC10237035, truy cập **200**. Tìm kiếm web nêu supplementary có dữ liệu GPS-ORFeome kèm PSI và thay đổi dưới MLN7243/bortezomib. `[CHƯA XÁC MINH]` có đột biến điểm hay không.
- `[ĐO]` **bioRxiv 09/2026 — "Single Amino Acid Disease Mutations Act as Genetic Glues"**, [DOI 10.64898/2026.09.17.752235](https://doi.org/10.64898/2026.09.17.752235), truy cập **200**. Tìm kiếm web nêu 79 biến thể phá degron theo |Δlog₂FC(Mut−WT)| ≥ 1,5 và **saturation mutagenesis của degron lõi ZNF711**. Đây là nguồn mới nhất và gần bài toán nhất về mặt câu hỏi (hiệu ứng đột biến điểm lên degron), nhưng là **tiền ấn phẩm chưa phản biện** và endpoint là log₂FC, không phải PSI. Xếp T1/T3 lai; kiểm trước khi tin.
- `[CHƯA XÁC MINH]` Phần **saturation mutagenesis cho 219 degron phụ thuộc CRL** mà tìm kiếm web gán cho luận án đi kèm Zhang 2023. Nếu đúng, đây có thể là **cùng thư viện 28-mer** với nhãn chính — tức ứng viên T1 lý tưởng nhất. Hiện bộ bão hòa thô của đề tài có 249 peptide, benchmark dùng 91 sau lọc, nên cần kiểm: 219 này là tập con đã có trong `data/raw/` hay là bộ khác chưa tải. **Kiểm trước khi đi tìm nguồn ngoài.**

## 3. Ứng viên T2–T4 — xếp hạng và lý do

| Nguồn | Tầng | Trạng thái `[ĐO]` | Vai trò đề xuất |
|---|---|---|---|
| **Voutsinos 2026** (đã có tại máy, MIT) + bản bioRxiv [DOI 10.1101/2025.05.10.653233](https://doi.org/10.1101/2025.05.10.653233) nêu **>200.000 tile 30-residue** từ hơn 5.000 protein bào tương, phủ 99,7% | T2 | Đã ở `data/raw/voutsinos-2026/` | **Nguồn tiền huấn luyện chính của P3.** Lớn, cùng ý tưởng đo, đã có quyền MIT |
| **Larsen 2025** TF tile (đã có tại máy) | T2 | Quyền phủ dữ liệu `[CHƯA XÁC MINH]`, chờ email | Chỉ kiểm chuyển miền, sau khi quyền chốt |
| **Human Domainome 1**, Nature 2025, [DOI 10.1038/s41586-024-08370-4](https://doi.org/10.1038/s41586-024-08370-4) — aPCA ~500 domain người, site-saturation | T3 | **200** | Kiểm chuyển miền quy mô lớn ở mức residue. Endpoint là **độ dồi dào khi gập**, không phải tín hiệu degron → tách hoàn toàn khỏi thang ΔPSI |
| **MaveDB / ProteinGym** — VAMP-seq và DMS độ dồi dào: PTEN, TPMT, NUDT15, CYP2C9/19, ASPA ([DOI 10.1038/s41467-024-48481-0](https://doi.org/10.1038/s41467-024-48481-0)), Parkin ([DOI 10.1038/s41467-024-45829-4)](https://doi.org/10.1038/s41467-024-45829-4) | T3 | MaveDB đã có 26 score set tại máy (CC0); ProteinGym **200**; hai bài Nat Commun **200** | **Kiểm chứng ngoài cho ca nghiên cứu**, đúng như đề cương đã ghi. ASPA và Parkin đáng chú ý riêng: cả hai có phần **tile degron** bên cạnh DMS độ dồi dào, nên là cầu nối T2–T3 hiếm có |
| **Tsuboyama 2023** K50/ΔG ([Zenodo 7844779](https://zenodo.org/records/7844779)) và **MGnify Stability** 2026 (~1,8 M domain) | T3 phụ | Zenodo **200** (yêu cầu đăng ký tải) | **Đối chứng gây nhiễu**, không phải nhãn. Dùng để phân biệt "đột biến phá degron" với "đột biến phá gập domain". Lưu ý: nhãn chính là peptide tách rời, không có domain gập, nên vai trò này chỉ xuất hiện khi diễn giải biến thể protein nguyên vẹn |
| **ELM** | T4 | Trang downloads **200**; Academic License đã đọc | Prior motif (P2 của khuyến nghị 21/10), chỉ nội bộ. Không vào ứng dụng công khai |
| **DEGRONOPEDIA** | T4 | Trang `/download` **404**, trang documentation **200** | Đối chiếu chức năng. Không nhập hàng loạt |
| **MetaDegron, DegronMD** | T4 | Đã audit 21/10 | Giữ nguyên kết luận 21/10: chưa nhập train chính |
| **Nat Cell Biol 2023** multiplex CRISPR E3–substrate, [DOI 10.1038/s41556-023-01229-2](https://doi.org/10.1038/s41556-023-01229-2) | T4 | **200** | Chỉ đáng xét nếu nhánh E3 được mở lại — mà audit 21/10 cho thấy cổng dữ liệu E3 **chưa đạt** (sau lọc chỉ 1–2 nhóm có ≥5 mẫu) |

`[DIỄN GIẢI]` Điểm cần nói rõ về T3: thêm DMS độ dồi dào **không** tháo được nút thắt của G2. Nhãn chính hỏi "phép thay này làm tín hiệu degron mạnh hay yếu", còn VAMP-seq/aPCA hỏi "biến thể này còn lại bao nhiêu protein", trong đó phần lớn biến thiên đến từ gập/không gập. Trộn hai thứ sẽ làm mô hình học sai đại lượng. Vì vậy T3 vào kế hoạch ở vai **kiểm chứng ngoài và đối chứng gây nhiễu**, không vào ngân sách nhãn huấn luyện.

## 4. Protocol xác minh trước khi tải bất kỳ nguồn nào

`[ĐỀ XUẤT]` Thứ tự bắt buộc — quyền trước, dữ liệu sau:

1. **Kiểm nội bộ trước — một phần đã làm, xem §0.** Phép đếm bộ lọc đã xong: 248 peptide thô, 144 bị chặn bởi ngưỡng degron. Việc còn lại là đối chiếu con số "219 degron CRL saturation" mà tìm kiếm web gán cho luận án đi kèm Zhang 2023 với 248 peptide này, bằng cách đọc lại `data/raw/I28 CRL Saturation Mutagenesis.zip` và `interim/zhang-saturation-unzip/`. Nếu 219 là tập con của 248 thì **không có nguồn ngoài nào cần tải cho T1 nội vùng**, và P0 đã là toàn bộ phần khai thác được.
2. **Đọc giấy phép từng nguồn**, ghi nguyên văn vào `data/README.md` §2: giấy phép bài báo **không** tự phủ file dữ liệu; supplementary của Cell/JCB/PNAS theo điều khoản nhà xuất bản, không phải CC mặc định chỉ vì bản PMC mở. Không rõ → ghi blocker, dừng.
3. **Tải vào thư mục riêng, rỗng**, ghi SHA-256 từng file vào manifest, đọc bằng `python -I`, không chạy mã từ trong thư mục nguồn.
4. **Audit nội dung trước khi dùng**: schema từng bảng; có PSI thô/count hay chỉ điểm đã xử lý; chiều của hiệu ứng; cách tạo mốc WT; số replicate; peptide dài bao nhiêu; thư viện nào.
5. **Audit chồng lặp**: ánh xạ về accession UniProt, gán cụm MMseqs2 id30/cov80 **bằng chính bảng cụm hiện có**, báo số **cụm mới thật** và số cụm trùng. Đây là số quyết định cổng P2, không phải số peptide.
6. **Kiểm thang đo** trước khi hợp nhất: so phân bố PSI và ΔPSI của nguồn mới với Zhang trên phần peptide/cụm trùng, nếu có. Lệch hệ thống → head riêng, không hợp nhất.
7. Cập nhật `data/README.md` (§2, §3, nhật ký §5) **trong cùng phiên** với lúc tải.

## 5. Kết luận khảo sát

`[DIỄN GIẢI]`

- **Việc rẻ nhất đã đo xong và nó thắng mọi nguồn ngoài về tỉ lệ giá trị/chi phí** (§0): 85 peptide thêm được ngay bằng cách nới một hằng số, không tải gì, không cần quyền mới. Làm P0 trước khi tải bất kỳ thứ gì.
- Tầng dữ liệu **ngoài repo** có giá trị cao nhất mà đề tài chưa khai thác là T1: saturation mutagenesis **cùng hệ GPS/PSI** ở các lớp degron khác. Nó tồn tại và truy cập được qua PMC — cụ thể là Koren 2018 Table S4.
- Các nguồn T3 (Domainome, MaveDB/ProteinGym, Tsuboyama) **không** thay được nhãn ΔPSI và không nên vào ngân sách huấn luyện; chúng vào luận văn ở phần kiểm chứng ngoài và phân tích giới hạn.
- Không có nguồn nào trong khảo sát này đủ điều kiện để nhập vào huấn luyện **ngay hôm nay**: mỗi nguồn còn thiếu ít nhất một trong hai thứ — quyền sử dụng đã đọc, hoặc audit nội dung bảng.
- `[ĐO]` Với ứng viên số 1 (Koren 2018 Table S4), đã kiểm xong **cả hai** và kết quả là: tải bị chặn bằng cơ chế chống bot, và nguồn **không có giấy phép mở** (§2b). Việc tiếp theo cho nguồn này là việc làm tay của người, không phải việc của script.
- `[DIỄN GIẢI]` Kết quả [phần C của thí nghiệm đường cong học](../learning-curve-2026-10-22/README.md) đổi **lý do** cần nguồn ngoài: mở rộng phân bố *trong cùng thư viện Zhang* đã hết lợi ích quanh ngưỡng degron 4,0, nên giá trị của Koren 2018 nằm ở chỗ nó là **lớp degron khác** (đầu C), không ở số ô nó thêm.

## 6. Tái lập lượt khảo sát

Kiểm truy cập:

```bash
.venv/bin/python -I topics/degron-footprint/research/next-steps-plan-2026-10-22/check_candidate_access.py
```

Script chỉ gửi HEAD/GET tới trang công bố, **không tải payload**, không gửi chuỗi của đề tài lên server. Kết quả ghi `candidate-access.json` kèm ngày kiểm. Status 200 nghĩa là endpoint trả nội dung, **không** nghĩa là dữ liệu dùng được hay giấy phép cho phép nhập.

Truy vấn PubMed đã dùng (qua MCP, 22/10/2026):

```
(degron[Title/Abstract] OR "protein stability index"[Title/Abstract])
  AND (saturation mutagenesis[Title/Abstract] OR "deep mutational scanning"[Title/Abstract]
       OR "global protein stability"[Title/Abstract])            -> 12 kết quả, từ 2018
(dipeptidyl peptidase AND N-degron AND E3)
  OR ("N-terminal cysteine" AND degradation AND global profiling) -> 4 kết quả, từ 2023
```

Truy vấn web đã dùng: DMS độ dồi dào/VAMP-seq mức residue; saturation mutagenesis degron GPS PSI 2024–2025; Koren/Timms C-degron N-degron supplementary PSI; Tsuboyama K50/ProteinGym; degron DMS 2026. Danh mục kết quả không được lưu lại máy; coi §2–§3 là bản ghi của lượt này.

Nguồn metadata bài báo: PubMed (qua MCP `pubmed`), DOI ghi kèm từng mục ở trên.
