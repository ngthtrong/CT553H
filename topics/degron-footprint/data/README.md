# Dữ liệu của đề tài `degron-footprint` — nguồn gốc và quá trình xử lý

> File này là **sổ nguồn gốc** của thư mục `data/`: mỗi file đến từ đâu, phiên bản nào, giấy phép gì, ai/script nào tạo ra, và đã xử lý qua những bước nào. Nội dung `data/` bị `.gitignore` chặn; **riêng file này được lên git** (ngoại lệ `!**/data/README.md`).
>
> Cập nhật lần cuối: **22/10/2026** (thêm hai cache của thí nghiệm đường cong học; không tải nguồn mới). Dung lượng trước phiên G2 ≈ **2,3 GB** (`raw/` 1,2 GB · `interim/` 1,1 GB · `processed/` 123 MB).
>
> **Khi thêm, xử lý lại hoặc xoá file trong `data/`:** sửa bảng ở mục 3 (và mục 4 nếu đổi định dạng tập huấn luyện), rồi thêm một dòng vào nhật ký mục 5.

Mọi đường dẫn script bên dưới tương đối với thư mục đề tài `topics/degron-footprint/`. Mọi lệnh chạy từ **thư mục gốc repo** với `.venv/`.

## 1. Quy ước ba tầng

| Tầng | Ý nghĩa | Được phép |
|---|---|---|
| `raw/` | Bản gốc tải về, **không sửa tay**. Mỗi nguồn có manifest kèm SHA-256 | Chỉ thêm file mới; không ghi đè |
| `interim/` | Giải nén, cache, file tạm của công cụ (MMseqs2) | Xoá được, dựng lại từ `raw/` |
| `processed/` | Đầu ra của script trong `research/` | Xoá được, **phải** sinh lại được bằng script ghi ở mục 3 |

Dữ liệu tải về là dữ liệu không tin cậy: đọc bằng `python3 -I`, không chạy script từ bên trong `raw/` (đặc biệt repo `voutsinos-2026/repo/` chứa mã của bên thứ ba).

## 2. Nguồn gốc

| # | Nguồn | Định danh / phiên bản ghim | Giấy phép | Ngày tải | Nằm ở | Kiểm toàn vẹn |
|---|---|---|---|---|---|---|
| 1 | **Zhang et al. 2023**, *Molecular Cell* — đột biến quét, bão hòa, sàng peptidome GPS, CRISPR. [Ghi chép bài](../../../resources/papers/analyzed-papers/zhang-2023.md) | Mendeley Data [`10.17632/32h94v2yv2.2`](https://data.mendeley.com/datasets/32h94v2yv2/2) (phiên bản 2), cả 5 file | **CC BY 4.0** (dữ liệu); bài báo All rights reserved | 12/10 (2 file), 13/10 (đủ 5) | `raw/*.zip`, `raw/Zhang et al., Raw Image Data Compiled.pdf` | SHA-256 **khớp checksum Mendeley công bố** — `raw/full-download-manifest.json` → `mendeley` |
| 2 | **Zhang et al. 2023** — bảng PSI peptidome | NCBI GEO [`GSE240610`](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE240610): Table S1 + `GSE240610_RAW.tar` (60 file count) + `filelist.txt` | Theo điều khoản GEO (công khai) | 13/10 | `raw/geo-gse240610/` | GEO không công bố checksum; SHA-256 ghi lúc tải — manifest → `geo` |
| 3 | **Voutsinos et al. 2026**, *Science Advances* ([DOI 10.1126/sciadv.adz3483](https://doi.org/10.1126/sciadv.adz3483)) — thư viện tile bào tương, điểm degron, mô hình PAP. [Ghi chép bài](../../../resources/papers/analyzed-papers/voutsinos-2026.md) | GitHub [`KULL-Centre/_2025_Voutsinos_degron_cytosol`](https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol) @ **`9b3eafa6bd9730c558cd018063fa0180edf9db1a`** (main, 06/03/2026) | **MIT** (mã + dữ liệu trong repo); bài báo CC BY-NC 4.0 | 13/10 | `raw/voutsinos-2026/repo/` (50 file) | Kiểm `HEAD` đúng commit ghim; SHA-256 từng file — manifest → `voutsinos`. **Zenodo `16925278` trả 403 từ mạng này**, nên dùng repo GitHub cùng tác giả |
| 4 | **MaveDB** — 26 score set của 9 gene trong bài Voutsinos (PTEN, TPMT, NUDT15, CYP2C9, CYP2C19, ASPA, PRKN, GCK, LDLR). [Ghi chép](../../../resources/papers/analyzed-papers/mavedb.md) | API `api.mavedb.org/api/v1`, URN từng score set trong `raw/mavedb/score-sets.json` | **CC0** (cả 26 set, đọc từ metadata) | 13/10 | `raw/mavedb/` | MaveDB có thể cập nhật; SHA-256 ghi lúc tải — manifest → `mavedb` |
| 5 | **UniProtKB/Swiss-Prot** người (snapshot) | `rest.uniprot.org/uniprotkb/stream`, truy vấn `(organism_id:9606) AND (reviewed:true)`, **release 2026_03** | CC BY 4.0 | 12/10 | `raw/human-reviewed-2026-10-12.fasta.gz` | SHA-256 trong `raw/human-reviewed-2026-10-12.fasta.manifest.json`, script kiểm lại mỗi lần chạy |
| 6 | **UniProtKB** — 17 accession không có trong snapshot (đã đổi tên/gộp/rút) | `rest.uniprot.org/uniprotkb/<acc>.fasta`, ghi cả URL sau redirect | CC BY 4.0 | 12/10 | `raw/uniprot-additional/` | SHA-256 trong `raw/uniprot-additional/manifest.json` |
| 7 | **AlphaFold DB v6** — 8 cấu trúc protein MaveDB | `alphafold.ebi.ac.uk/files/AF-<acc>-F1-model_v6.pdb` (**cần User-Agent**, nếu không EBI trả 403) | CC BY 4.0 | 14/10 | `raw/alphafold/` | Số residue + SHA-256 trong `raw/alphafold/manifest.txt` |
| 8 | **Larsen et al. 2025** — bộ nhân, tile TF | GitHub `KULL-Centre/_2025_Larsen_degron_transcriptionfactors` tag **`v1.0`** (commit `2698ecc6`) | **MIT** (repo); ⚠ phủ cả file dữ liệu hay không **đang chờ xác nhận qua email** | 15/10 | `raw/larsen-2025/` | SHA-256 + audit trong [SOURCE.md](raw/larsen-2025/SOURCE.md) |
| 9 | **NCBI ClinVar** — phân loại biến thể lâm sàng | `ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz`, `Last-Modified` **12/10/2026**. ⚠ **Không có số phiên bản, ghi đè mỗi tuần** | ⚠ **Không có giấy phép kiểu CC** — chỉ **yêu cầu ghi công** + câu phủ nhận chẩn đoán phải đi theo đầu ra ứng dụng | 15/10 | `raw/clinvar/` | SHA-256 `a5198a11…28218`, nguyên văn điều khoản trong [SOURCE.md](raw/clinvar/SOURCE.md) |
| 10 | **MetaDegron**, *Briefings in Bioinformatics* 2024, DOI `10.1093/bib/bbae519`; repo, toàn văn, supplementary S1–S5, web và truy nguồn ELM | GitHub `BioDataStudy/MetaDegron` @ **`ca12c0cf9d2e2d76655689973ac45c6c063a899d`** (20/06/2024); PMC11491831 / Europe PMC supplementaryFiles | **Repo không có LICENSE: chưa xác nhận**; bài CC BY 4.0; quyền dữ liệu nhập từ ELM không suy ra từ giấy phép bài. Đã đọc ELM Academic License, chỉ dùng truy nguồn nội bộ; chưa nhập vào train/ứng dụng | 21/10 | `raw/metadegron/` | SHA-256 từng file dữ liệu/trọng số tải đủ, URL, lỗi truy cập, license và script trong [manifest](../research/metadegron-analysis-2026-10-21/source-manifest.json); [báo cáo](../research/metadegron-analysis-2026-10-21/README.md) |

**Thử tải 22/10, KHÔNG lấy được:** supplementary của **Koren et al. 2018** (Cell, DOI `10.1016/j.cell.2018.04.028`, PMC6003881) — nhắm Table S4 (saturation mutagenesis, cùng hệ GPS/PSI). Trang PMC đọc được và liệt kê 15 file, nhưng mọi lần tải `.xlsx` trả trang chờ `Preparing to download ...` cần bắt tay cookie bằng JavaScript; **không thực hiện bước đó**. `oa.fcgi` trả 404 ⇒ **không thuộc PMC Open Access Subset**, tức đọc tự do nhưng **không có giấy phép mở để phân phối lại**. Bằng chứng, giấy phép và đường đi còn lại: [raw/koren-2018-probe/SOURCE.md](raw/koren-2018-probe/SOURCE.md). Thư mục đó **không chứa dữ liệu nghiên cứu**, chỉ giữ trang chờ làm bằng chứng lỗi.

**Koren et al. 2018 — đã có dữ liệu (người dùng tải tay bằng trình duyệt, 22/10/2026), nguồn #: supplementary NIHMS967427.** Nằm ở `raw/koren-2018/` (sao từ `raw/koren-2018-probe/`, không di chuyển). Giấy phép: bản NIHMS, **không** thuộc PMC Open Access (`oa.fcgi` 404) → **chỉ dùng nội bộ**, không đưa bảng gốc lên git/phụ lục/nguyên mẫu công khai; `data/` đã gitignore. Kiểm toàn vẹn SHA-256 (tính tại máy sau khi tải, nguồn không công bố hash):

| File | Bảng (đã mở file xác nhận) | SHA-256 |
|---|---|---|
| `NIHMS967427-supplement-10.xlsx` | S3 (thế Ala, 5 clone) | `0514eb64b42989bbc20f2b2be2f4ab9852464002d210e2fdb531106c888393aa` |
| `NIHMS967427-supplement-11.xlsx` | **S4 (saturation mutagenesis, 9 substrate)** | `c96973f2b2781b35a822527fa875e38df82f75da9ac327668d1d10114fdbcbeb` |
| `NIHMS967427-supplement-12.xlsx` | S5 (danh sách substrate) | `6d4760bdd54594239b3423c740e1d34263b56bbeb6dd4bcedd7d890ea362eb90` |
| `NIHMS967427-supplement-13.xlsx` | S6 (sàng G-end) | `0c565d7d00e72045bccabaa012023bbcd93d4cb1af172ebf472f348120802f83` |
| `NIHMS967427-supplement-14.xlsx` | S7 (sàng 23-mer đầu C) | `a31902e637c9b149bf3344d93fb87b384a39a8b1ef562de4760a86894089e2ae` |
| `NIHMS967427-supplement-15.xlsx` | S8 (CRISPR) | `bbc119093c9f1dc6dc9633ec9f70ea3ac0775a5b23bce607c904d34924609aaa` |
| `nihms967427.pdf` | bản NIHMS của bài | `13b244c118b8bc2a39ee0129d7f35c5df375351509cfd799d96bbf95487cdc16` |

Script đọc: [`research/koren-s4-audit-2026-10-22/audit.py`](../research/koren-s4-audit-2026-10-22/audit.py) (chỉ `supplement-10`, `-11`; `python -I` + openpyxl `data_only`, không chạy mã trong file). Sinh `interim/koren-2018-cells.tsv` (bảng ô chuẩn hóa, 1.911 dòng: 1.739 ô S4 + 172 ô S3; cột `table, substrate, pos, wt_aa, mut_aa, psi, dpsi, n_bins`) và `interim/koren-2018-cluster/` (FASTA + MMseqs2 id30/cov80 liên hợp 6.573 protein Zhang + 5 protein Koren; chạy riêng, **không ghi đè** `protein-id30-cov80_cluster.tsv`). Kết luận: cổng P2 **không đạt** (5 cụm mới < 20); xem [báo cáo](../research/koren-s4-audit-2026-10-22/README.md).

**Chưa tải (không có trong `data/`):** read giải trình tự thô (SRA `PRJNA1277273` của Zhang); bản **archive** của ClinVar để ghim số liệu ([SOURCE.md §5](raw/clinvar/SOURCE.md)).

**Đã tải 18/10:** Degformer, commit `49ee524599671f2b5e30d9cd052ce6baa55c06d8`, Apache-2.0; [SOURCE/giấy phép nguyên văn](raw/degformer-isolated/SOURCE.md). Nguồn https://github.com/Alpine2048/Degformer; manifest SHA-256 từng file được giữ trong SOURCE và [manifest có version control](../research/g2-saturation-2026-10-18/source-manifest.json).

## 3. Danh mục từng file

### 3.1 `raw/`

**Bổ sung MetaDegron 21/10:** `metadegron/repo/` là clone ghim, không chạy mã tải về; `paper.{xml,html}`, `supplementary-files.zip`, `supplementary/*.xlsx` là nguồn đọc. Các URL XLSX lẻ trả HTML challenge và bảng review 2017 trả trang ELTEnet được giữ như bằng chứng lỗi, **không coi là dữ liệu truy cập được**. `web-*.html`, ảnh demo và ELM/license/snapshot truy nguồn giữ dưới `raw/`, không lên git. Hai file lớn SeqVec/embedding có endpoint HTTP 200 nhưng fetch thử bị giới hạn dung lượng, **không giữ payload, không có SHA đầy đủ**.

`metadegron/derived/` chứa bảng chuẩn hóa JSON, mẫu kiểm nguồn, FASTA protein và MMseqs2 cov50/cov80 kèm log/tmp; do [audit_dataset.py](../research/metadegron-analysis-2026-10-21/audit_dataset.py) sinh. Cụm protein hiện có của đề tài chỉ được đọc, không ghi lại. `xgboost-literal-state.json` được [safe-predict-x.py](../research/metadegron-analysis-2026-10-21/safe-predict-x.py) tách bằng đọc **literal byte UBJSON** trong pickle, không gọi unpickle/khởi tạo đối tượng từ file. Kết quả nhỏ/kiểm chéo nằm ở research; không tạo dữ liệu mới trong `processed/`, không đổi nhãn G2. Lệnh dựng lại và giới hạn: [VALIDATION.md](../research/metadegron-analysis-2026-10-21/VALIDATION.md).

**Bổ sung 18/10:** `degformer-isolated/{predict.py,train_v2.py,README.md,LICENSE,peptide_model_epoch50.pt,training_data.csv,manifest.json}` từ [download.py](../research/g2-saturation-2026-10-18/download.py); SHA từng file được kiểm. Không chạy top-level code nguồn. Training table có 569.270 dòng; dùng kiểm overlap, không dùng huấn luyện mô hình đề tài. Checkpoint được nạp riêng qua `python -I`.


| File / thư mục | Nguồn (mục 2) | Tạo bởi | Ghi chú |
|---|---|---|---|
| `I28 Scanning Mutagenesis.zip` (27,9 MB) | 1 | `research/e3-labels-audit/fetch_scanning.py` (12/10), kiểm lại bởi `fetch_all.py` | Đột biến quét: 3 điều kiện (Replicate 1, Replicate 2, BAG6 WT) × 6 bin count + CSV PSI tác giả tính sẵn **chỉ cho Replicate 1** |
| `I28 CRL Saturation Mutagenesis.zip` (5,2 MB) | 1 | như trên | Đột biến bão hòa: 12 file count `S1..S12` |
| `I28 GPS Peptidome Screen and MLN4924 and SVM.zip` (393 MB) | 1 | `research/full-data-audit/fetch_all.py` (13/10) | 18 file count, PSI ba điều kiện, **hai file dự đoán PSI bằng SVM của chính tác giả** |
| `Degron CRISPR Screens.zip` (2,6 MB) | 1 | `fetch_all.py` (13/10) | Kết quả MAGeCK của 31 screen CRISPR (+3 control), 68 file. Đã phân tích ở [e3-labels-audit](../research/e3-labels-audit/README.md) (giải nén ra thư mục tạm, không lưu ở `interim/`) |
| `Zhang et al., Raw Image Data Compiled.pdf` (1 MB) | 1 | `fetch_all.py` (13/10) | Ảnh thô của bài; chưa dùng |
| `download-manifest.json` | 1 | `fetch_scanning.py` (12/10) | Manifest cũ, chỉ 2 file ZIP; bị thay về nội dung bởi `full-download-manifest.json` |
| `full-download-manifest.json` | 1–4 | `fetch_all.py` (13/10) | **Manifest chính**: URL, kích thước, SHA-256 từng file của bốn nguồn Mendeley/GEO/Voutsinos/MaveDB |
| `mendeley-files.json` | 1 | Lưu tay 12/10 (không có script) | Ảnh chụp phản hồi API `public-api/datasets/32h94v2yv2/files?version=2`, có `sha256_hash` do Mendeley công bố |
| `mendeley-v2-page.html` | 1 | Lưu tay 12/10 (không có script) | Ảnh chụp trang dataset; chỉ để đối chiếu |
| `geo-gse240610/` | 2 | `fetch_all.py` (13/10) | Table S1 (52,9 MB, 475.507 dòng × 3 sheet), `RAW.tar` (21,9 MB), `filelist.txt`. `RAW.tar` **chưa dùng** |
| `voutsinos-2026/repo/` | 3 | `fetch_all.py` (13/10), `git clone` + `checkout` commit ghim | Có `.git/`. Dùng: `score/degrons.csv.gz`, `models/degron_train.csv.gz`, `models/pap_weights.tgz`, `library/*` |
| `mavedb/` (53 file) | 4 | `fetch_all.py` (13/10) | Mỗi score set một `*.scores.csv` + `*.json` metadata; danh mục `score-sets.json` |
| `human-reviewed-2026-10-12.fasta.gz` + `.manifest.json` | 5 | `research/e3-labels-audit/prepare_protein_clusters.py` (12/10) | Chỉ tải nếu chưa có; lần sau script chỉ kiểm SHA-256 |
| `uniprot-additional/` | 6 | `prepare_protein_clusters.py` (12/10) | 17 accession: 8 lấy được qua redirect (ví dụ P10316, P16188 → P04439 HLA-A), **9 trả rỗng** (đã rút, SHA-256 = hash của chuỗi rỗng) |
| `alphafold/` | 7 | `curl` tay theo [architecture-check](../research/architecture-check/README.md) (14/10) | 8 file PDB + `manifest.txt` |
| `mmseqs-id30-cov50.log`, `mmseqs-id30-cov80.log` | — | `prepare_protein_clusters.py` (12/10) | Log MMseqs2. Lẽ ra thuộc `interim/`; để nguyên vì script ghi vào đây |
| `composition-audit-run.log`, `composition-audit-cov50-run.log` | — | stdout của `research/e3-labels-audit/audit_composition.py` (12/10), không / có `--clusters` | Log chạy; kết quả chính thức là JSON trong `research/e3-labels-audit/` |

### 3.2 `interim/`

| File / thư mục | Dựng lại bằng | Ghi chú |
|---|---|---|
| `zhang-scanning-unzip/` (162 MB) | `unzip -oq "raw/I28 Scanning Mutagenesis.zip" -d interim/zhang-scanning-unzip` | Đầu vào của `build_psi.py` |
| `zhang-saturation-unzip/` (37 MB) | `unzip -oq "raw/I28 CRL Saturation Mutagenesis.zip" -d interim/zhang-saturation-unzip` | Đầu vào của `build_psi.py` |
| `zhang-gps-unzip/` (777 MB) | `unzip -oq "raw/I28 GPS Peptidome Screen and MLN4924 and SVM.zip" -x "*.xlsx" -d interim/zhang-gps-unzip` | Đầu vào của `gps_peptidome_audit.py`. Bỏ `.xlsx` (đã có Table S1 từ GEO) |
| `scanning-replicate-1.csv` (64 MB) | Bản chép của `I28 Scanning Mutagenesis Replicate 1.csv` trong ZIP quét | **SHA-256 trùng khớp** với file trong `zhang-scanning-unzip/` (`a5937f4c…`). Bản thừa, xoá được |
| `pap-weights/pap_weights/` | `tar -xzf raw/voutsinos-2026/repo/models/pap_weights.tgz -C interim/pap-weights` (14/10) | `cnn2w1_weights.h5`, `cnn2w7_weights.h5`. Đầu vào của `pap_baseline.py`, `architecture_check.py` |
| `protein-id30-cov{50,80}_{cluster.tsv,rep_seq.fasta,all_seqs.fasta}` | `prepare_protein_clusters.py --coverage 0.5` / `0.8` (12/10) | Cụm MMseqs2 `easy-cluster`, identity ≥ 0,3, coverage hai chiều 0,5/0,8. cov50: **4.418** cụm; cov80: **5.088** cụm, trên 6.573 protein (`research/e3-labels-audit/protein-clusters-cov*.json`) |
| `protein-id30-cov50-tmp/`, `mmseqs-id30-cov80/` | — | Thư mục tạm của MMseqs2, **ghi đường dẫn tuyệt đối cũ**. Xoá được; nếu cần thì chạy lại `prepare_protein_clusters.py` |
| `protein-id30-cov80-proteome_cluster.tsv` (CC BY 4.0, dẫn xuất từ UniProt) | `research/r3-domain-gate-2026-10-22/build_proteome_clusters.py` (22/10) | Phân cụm MMseqs2 id30 cov80 (**cùng cờ** với bản gốc) trên **toàn** snapshot UniProt 20.431 protein → 12.918 cụm. Khác `protein-id30-cov80_cluster.tsv` (chỉ 6.573 protein của các thí nghiệm). Dùng cho R3 (sàng peptidome 18.753 protein). Manifest SHA-256: `research/r3-domain-gate-2026-10-22/proteome-cluster-manifest.json`. Xoá được, dựng lại ~10 phút |
| `gps-peptidome-rep1.tsv` (21 MB, 475.506 dòng) | `research/variant-coverage-2026-10-15/coverage.py` tự dựng nếu thiếu (15/10, phiên 10) | Cache của sheet **`I28 Control Replicate 1`** trong Table S1 GEO. Cột `peptide reads psi`. Chỉ là cache để khỏi đọc lại `.xlsx` 52,9 MB (openpyxl rất chậm trên 475k dòng); xoá được |

### 3.3 `processed/`

**Bổ sung 22/10 — đường cong học**, sinh bởi [run_curve.py](../research/learning-curve-2026-10-22/run_curve.py). **Không nguồn dữ liệu mới**: cả hai file dựng lại từ `residue_data.load_all(degron_psi_max=...)`, tức cùng các bảng `psi-sat_{a,b}.tsv`, CSV quét, UniProt ghim và `protein-id30-cov80_cluster.tsv` như cache G2.

- `learning-curve-sat-base.npz` (1,2 MB): bộ bão hòa ở ngưỡng degron **3,0** hiện hành — 91 peptide, 47.847 ô. Khóa: `X` (47.847×180, **chỉ** đặc trưng M3, **không** có cột ΔPAP), `y`, `idx`, `peps`, `groups`, `rowg`, `wtkeys`/`wtvals` (PSI WT từng peptide).
- `learning-curve-sat-ext4.0.npz` (2,3 MB): cùng schema, ngưỡng degron nới lên **4,0** — 176 peptide, 92.337 ô. Dùng cho thí nghiệm P0; 85 peptide chênh lệch chỉ vào outer-train, không bao giờ vào outer-test.
- `learning-curve-sat-ext{3.5,4.5,5.0}.npz`: cùng schema, ngưỡng 3,5 / 4,5 / 5,0 — thêm lần lượt 50 / 106 / 121 peptide so với bộ base. Sinh bởi [run_sensitivity.py](../research/learning-curve-2026-10-22/run_sensitivity.py) cho lưới độ nhạy phần C.

Khác với `g2-saturation-input.npz`: hai file này **không** chứa ΔPAP nên không cần trọng số PAP/Keras; đổi lại chúng không dùng được cho các mô hình có nhánh ΔPAP. Mốc ΔPAP 0,7693 được dẫn lại từ G2, không tính lại. Tiêu chí chốt trước ở [PROTOCOL.md](../research/learning-curve-2026-10-22/PROTOCOL.md); kết quả `results.json` nằm ở research. Cả hai NPZ bị gitignore, xoá được, runner tự dựng lại.

**Bổ sung 22/10 — hiệu chuẩn P6**, sinh bởi [run_calibration.py](../research/calibration-p6-2026-10-22/run_calibration.py) và [build_model.py](../research/calibration-p6-2026-10-22/build_model.py). **Không nguồn dữ liệu mới, không dùng Koren**: chỉ đọc lại `learning-curve-sat-{base,ext4.0}.npz`. Ba file bị gitignore, sinh lại được:

- `calibration-p6-oof.npz`: điểm thô và xác suất platt/iso OOF theo seed trên 47.847 ô outer-test, hệ số ridge và alpha của 15 mô hình (seed × fold), chỉ số ô test từng fold.
- `calibration-p6-model.npz`: mô hình nguyên mẫu G3 (ridge M3 khớp trên 176 peptide / 92.337 ô + bộ hiệu chuẩn platt và iso). Đọc bởi `predict.py`.
- `calibration-p6-trainpath.npz`: điểm và xác suất theo đường huấn luyện (sklearn) trên 92.337 ô, để `verify.py` đối chiếu.

**Bổ sung 22/10 — tiền huấn luyện P3**, sinh bởi [build_exclusion.py](../research/pretrain-p3-2026-10-22/build_exclusion.py) và [run_p3.py](../research/pretrain-p3-2026-10-22/run_p3.py). **Không nguồn dữ liệu mới**: chỉ đọc `raw/voutsinos-2026/repo/{score/degrons.csv.gz,library/biomart_cytosol.csv.gz}`, UniProt ghim, cụm cov80 và hai cache `learning-curve-sat-{base,ext4.0}.npz`. Các file dưới bị gitignore, sinh lại được:

- `p3-tile-exclusion.json`: với từng gene Voutsinos (ENSG), tập protein thuộc 89 cụm outer-test mà nó chạm theo ba luật (MMseqs2 id≥0,30 alnlen≥50; trùng 12-mer; trùng tên gene) + bảng protein→cụm. Tóm tắt nhỏ nằm ở research (`exclusion-summary.json`).
- `p3-progress.pkl`: tiến độ chạy (dự đoán outer-test từng nhánh/lr/seed/fold, thống kê tiền huấn luyện), để chạy lại tiếp tục được.
- `p3-pretrained/p3-pre-seed{17,29,43}-fold{0..4}.pt`: 15 trọng số `Gate` sau tiền huấn luyện tile (nhỏ, vài chục KB mỗi file).

**Bổ sung G2 18/10**, sinh bởi [run.py](../research/g2-saturation-2026-10-18/run.py):

- `g2-saturation-input.npz`: `X` (47.847×181, 180 đặc trưng M3 + ΔPAP mutant−WT), `y` (ΔPSI trung bình hai nửa), `idx` (91 cặp start/end của peptide), `peps`, `groups` (cov80), `rowg` (cụm từng ô), `seqs` (mutant sequence), `wt` (WT sequence từng ô). Nguồn: `residue_data.load_all()`, PSI sat_a/sat_b, CSV quét để lấy trình tự tham chiếu, UniProt ghim, `protein-id30-cov80_cluster.tsv`, trọng số PAP `cnn2w1_weights.h5`. Không dùng nhãn scanning để huấn luyện phiên này.
- `g2-saturation-{ridge,gate_pap,no_gate_pap,gate_no_pap}-predictions.npz`: `seeds` và `predictions` (3×47.847), điểm OOF đúng cùng thứ tự ô của input.
- `g2-saturation-predictions.npz`: mỗi key là tên mô hình (gồm DeltaPAP, Degformer); điểm ensemble hoặc frozen, dài 47.847.
- `g2-saturation-models/*.pt`: 45 checkpoint mạng, kèm config, seed, epoch và chỉ số train/validation/test. Không phải model triển khai train trên toàn bộ dữ liệu.

Kiểm [audit.py](../research/g2-saturation-2026-10-18/audit.py): cỡ mẫu 91/89/47.847, dự đoán hữu hạn, outer test clusters rời nhau, tái lập ΔPAP 0,7692837467; bootstrap ghép cặp cụm. Kết quả JSON/log nhỏ nằm ở research. Bản tải và mọi NPZ/PT bị gitignore.

**Bổ sung G2 mở rộng 18/10 (phiên sau)**, sinh bởi [run_ext.py](../research/g2-extension-2026-10-18/run_ext.py). **Không nguồn dữ liệu mới**: cả ba thí nghiệm đọc lại `g2-saturation-input.npz` và `data/raw/degformer-isolated/`.

- `g2-ext-{bilinear,film}-predictions.npz`: `seeds` (17/29/43) và `predictions` (3×47.847), điểm OOF cùng thứ tự ô với input.
- `g2-ext-cross_ridge-predictions.npz`: `predictions` (47.847). Mô hình tất định nên chỉ một lượt, không có trục seed.
- `g2-ext-degformer_arch-predictions.npz`: `predictions` (47.847) và `seed`. Điểm ô là `pred(mutant) − pred(wild type)` của transformer huấn luyện lại; mục tiêu huấn luyện là **PSI tuyệt đối** chuẩn hoá z theo outer-train, nên file này **không cùng thang** với các mô hình học thẳng ΔPSI — chỉ dùng để xếp hạng (AUROC bất biến với phép đổi thang affine dương).
- `g2-ext-models/*.pt`: checkpoint của `bilinear`, `film` (3 seed × 5 fold mỗi loại) và `degformer_arch` (1 seed × 5 fold), kèm seed, epoch, chỉ số train/validation/test, và `target_mean`/`target_sd` cho `degformer_arch`.

Tiêu chí của ba thí nghiệm được chốt trước ở [PREREGISTRATION.md](../research/g2-extension-2026-10-18/PREREGISTRATION.md); JSON kết quả `e1-overlap.json`, `e2-candidates.json`, `e3-degformer-arch.json` nằm ở research. Mọi NPZ/PT ở đây bị gitignore.


| File | Sinh bởi | Đầu vào | Ghi chú / kiểm |
|---|---|---|---|
| `psi-rep1.tsv` (261.868 id), `psi-rep2.tsv` (261.999), `psi-wt.tsv` (264.036) | `research/full-data-audit/build_psi.py --condition all --validate` (13/10) | `interim/zhang-scanning-unzip/` | Cột `id psi sum nb1..nb6`. **Cổng kiểm:** dựng lại PSI Replicate 1 từ count thô và so với CSV tác giả, lệch lớn nhất **5,0 × 10⁻⁷** trên 261.865 giá trị → đạt (`research/full-data-audit/psi-build.json`) |
| `psi-sat_a.tsv` (134.608), `psi-sat_b.tsv` (134.563) | như trên | `interim/zhang-saturation-unzip/` | `sat_a` = file S1–S6, `sat_b` = S7–S12; giả định hai nửa là hai replicate đã kiểm bằng tương quan PSI **0,9544** |
| `composition-peptides.csv` | `research/e3-labels-audit/audit_composition.py` (12/10) | `raw/I28 Scanning Mutagenesis.zip` (đọc thẳng từ ZIP) | Chỉ số theo peptide, ngưỡng reads ≥ 10 |
| `protein-accessions.txt` (6.582 accession) | như trên | như trên | Đầu vào của `prepare_protein_clusters.py` |
| `proteins-full.fasta` (6.573 protein) | `prepare_protein_clusters.py` (12/10) | `raw/human-reviewed-*.fasta.gz` + `raw/uniprot-additional/` | Trình tự **hiện hành** của UniProt, không phải bản lịch sử lúc dựng thư viện. 9 accession thiếu được **loại**, không gán cụm riêng |
| `proteins-reviewed.fasta` (6.565), `missing-reviewed-accessions.txt` (17) | Phiên 12/10, **bản sớm hơn** của bước lấy trình tự; không còn script nào trong repo tạo ra | snapshot Swiss-Prot | Đã kiểm: mọi trình tự trùng với `proteins-full.fasta`. Bản lịch sử, bị thay bởi `proteins-full.fasta` |
| `r3-sat-wt-pool.tsv` (CC BY 4.0, dẫn xuất từ Zhang 2023) | `research/r3-domain-gate-2026-10-22/local_analysis.py` (22/10) | Nhãn miền cho R3: 235 peptide bão hòa sau lọc kỹ thuật (không áp ngưỡng degron), cột `peptide, psi_wt_internal, in_176, accession, cluster_cov80` (cụm theo phân cụm toàn proteome). Xoá được |
| `packages/degron-data-v1.zip`, `packages/degron-code-<commit>[-dirty].zip` (+ `.sha256`) | `research/notebook-kit-2026-10-22/make_data_package.py`, `make_code_package.py` (22/10) | **Gói để Trọng tự upload lên Kaggle/Colab.** Gói dữ liệu chỉ chứa nguồn được phép phân phối lại (Zhang/GEO công khai-trích dẫn, Voutsinos MIT, UniProt CC BY, Degformer Apache-2.0, cache dẫn xuất); từ chối cứng Koren/MetaDegron/Larsen/ClinVar. Manifest SHA-256 từng file trong `DATA_MANIFEST.json` ở trong zip. `CLAUDE.md` và `data/README.md` trong gói mã chỉ là stub. **Chưa upload gì**; xoá được, dựng lại bằng hai script |
| `r12-seqtable.npz` (0,9 MB), `r1-row-exclusion.npz` (2,0 MB) | `research/r2-esm-features-2026-10-22/make_seqtable.py`, `research/r1-degformer-clean-2026-10-22/build_exclusion_r1.py` (22/10) | cache `learning-curve-sat-{base,ext4.0}.npz`, `raw/degformer-isolated/training_data.csv`, `raw/human-reviewed-*.fasta.gz`, `proteins-full.fasta`, `interim/protein-id30-cov80_cluster.tsv` | Chuẩn bị cho R1/R2 (chưa huấn luyện). `r12-seqtable`: `peps, groups, wt_seq, idx, pos, aa, mut_seq, pep_of_row, y, base_n`. `r1-row-exclusion`: `excl, E1, E2, E3` (bool, 5 × 569.270), `group` (int64), `train_sha256`. Xoá được, dựng lại bằng hai script trên |
| `r6-scantable.npz` (1,9 MB; SHA-256 `09e1e308…9b30` lúc dựng 23/10) | `research/r6-ladder-scan-2026-10-23/make_scantable.py` (23/10) | `processed/psi-rep1.tsv`, CSV quét Replicate 1, UniProt ghim, `interim/protein-id30-cov80_cluster.tsv` (qua `residue_data.load_all(degron_psi_max=4.0)`) | Một dòng cho mỗi ô scanning của R6: **4.802 peptide / 133.764 ô / 2.902 cụm cov80** (PSI(WT) ≤ 4,0; ≥ 21 vị trí; reads ≥ 10; 7 peptide thiếu cụm bị loại). Khóa: `peps, wt_seq, psi_wt, groups` (theo peptide), `pep_of_row, pos, aa, mut_seq, y` (theo ô; `y` = ΔPSI so với WT đo trực tiếp `_mut0`). Thay thế chỉ R (64%) / A (23%) / S (12%). Sinh lại được; vào gói dữ liệu v2 |
| `footprint-rerun.json` | `research/e3-labels-audit/count_footprints.py` (chạy lại 12/10) | CSV Replicate 1 | **Trùng byte** với `research/e3-labels-audit/footprint-audit.json` (2.624 footprint). Bản thừa |
| `clinvar-scan-hits.json` (4,5 MB) | `research/variant-coverage-2026-10-15/coverage.py` (15/10, phiên 10) | `raw/clinvar/variant_summary.txt.gz` + bộ quét | Một dòng cho mỗi biến thể ClinVar rơi vào peptide degron bộ quét (18.691 dòng): gene, accession, vị trí protein, ref/alt, ý nghĩa lâm sàng, peptide, offset trong peptide, **vị trí đó có nhãn hay không** |
| `clinvar-driver-variants.json` (1,4 MB) | như trên | như trên | 4.875 biến thể trong 8 gene degron lái ung thư được kiểm điểm, kèm cờ thuộc từng tầng. Dùng cho [§7 của báo cáo](../research/variant-coverage-2026-10-15/README.md) |

## 4. Các trường của tập huấn luyện chính

Theo D-025, nhãn chính lấy từ **bộ bão hòa** (`psi-sat_a.tsv`, `psi-sat_b.tsv`), còn **bộ quét** (`psi-rep1.tsv`, `psi-rep2.tsv`) là nguồn phụ. Nhãn dùng là trung bình hai replicate. Cả hai bộ là **peptide 28-mer gắn vào đầu C của GFP** trong hệ GPS (Global Protein Stability) của Zhang 2023: tế bào được sort thành **6 bin** theo tỉ lệ GFP/DsRed, bin 1 là kém bền nhất, bin 6 là bền nhất. Peptide càng nằm ở bin thấp thì càng bị phân hủy nhanh.

### 4.1 Định danh `id` (chung cho mọi bảng)

Ví dụ: bộ quét `A0A0B4J271_TRAV12-3_4_mut13`, bộ bão hòa `A2RUQ5_C17orf102_2_mut10a`.

| Phần | Ví dụ | Ý nghĩa |
|---|---|---|
| Accession | `A2RUQ5` | Accession UniProt; trình tự dùng `processed/proteins-full.fasta` |
| Gene | `C17orf102`, `TRAV12-3` | Ký hiệu gene; có thể chứa `-`, nên tách id **từ phải sang** |
| Tile | `2` | Số thứ tự tile `n` trong protein; tile bắt đầu ở residue `(n−1)×23 + 1`, dài 28 |
| `mut` + vị trí | `mut10` | Vị trí đột biến 1..28 trong peptide; `mut0` = hoang dã (chỉ có ở bộ quét) |
| Amino acid thay vào | `a` | **Chỉ bộ bão hòa**: một trong 20 chữ thường `acdefghiklmnpqrstvwy` |

- **Peptide** = phần trước `_mut` (`<ACC>_<GENE>_<n>`). Accession là `id.split("_")[0]`; đây là khoá để gán **cụm protein cov80** khi chia train/test (`interim/protein-id30-cov80_cluster.tsv`, cột 1 = đại diện cụm, cột 2 = thành viên).
- Quy tắc tile (bước 23, dài 28 ⇒ hai tile liền nhau chồng 5 residue) suy từ bộ quét, khớp **128/130** peptide có trình tự thật; 2 ca lệch bị loại ([full-data-audit §6.1](../research/full-data-audit/README.md)).
- Regex đang dùng trong script: bộ quét `^(?P<pep>.+?)_mut(?P<pos>\d+)$`, bộ bão hòa `^(?P<pep>.+?)_mut(?P<pos>\d+)(?P<aa>[a-z])$`.

### 4.2 Bảng PSI dựng lại: `processed/psi-*.tsv`

Tab-separated, có header, một dòng một construct. Chỉ chứa id **có ít nhất một read**; construct không có read nào không xuất hiện (khác CSV của tác giả, xem 4.3).

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `id` | chuỗi | Định danh construct, mục 4.1 |
| `psi` | số thực, 1..6 | **Protein Stability Index** = `Σᵢ i × nbᵢ / sum`. **Thấp = bị phân hủy nhanh** (degron mạnh), cao = bền. Đây là nhãn |
| `sum` | số thực | `Σᵢ nbᵢ`, tổng read **sau chuẩn hoá**; dùng làm độ sâu đọc để lọc (bộ quét: ngưỡng `sum ≥ 10`) |
| `nb1`..`nb6` | số thực | Read đã chuẩn hoá ở bin 1..6: `nbᵢ = bᵢ × factorᵢ`, với `factorᵢ = Σ b₁ / Σ bᵢ` (tổng trên mọi construct của điều kiện, bin 1 làm chuẩn). Hệ số từng điều kiện ghi ở `research/full-data-audit/psi-build.json` |

| File | Bộ | Mẫu đếm gốc | Số id | Peptide |
|---|---|---|---:|---:|
| `psi-sat_a.tsv` | bão hòa, replicate A | `S1..S6` | 134.608 | 249 |
| `psi-sat_b.tsv` | bão hòa, replicate B | `S7..S12` | 134.563 | 249 |
| `psi-rep1.tsv` | quét, Replicate 1 | `S1..S6` (LIB054277) | 261.868 | 9.590 |
| `psi-rep2.tsv` | quét, Replicate 2 | `S7..S12` (LIB054277) | 261.999 | |
| `psi-wt.tsv` | quét, nền BAG6 WT | `S1..S6` (LIB057578) | 264.036 | |

**Bộ bão hòa — đặc thù:**

- Mỗi vị trí 1..28 được thay bằng **cả 20** amino acid (`aa` ∈ `acdefghiklmnpqrstvwy`), tức ma trận **28 × 20** mỗi peptide.
- **Không có `_mut0`**: không có phép đo hoang dã riêng. Ô mà `aa` trùng residue hoang dã ở vị trí đó là **construct đồng nghĩa** (đổi codon, giữ protein) và được dùng làm **WT nội tại**; mỗi peptide có 28 ô như vậy, SD PSI trong peptide trung vị 0,0576.
- **Không có cột trình tự**: residue hoang dã phải lấy từ `proteins-full.fasta` theo quy tắc tile ở 4.1.
- Nhãn đột biến: **ΔPSI = PSI(ô thay thế) − PSI(WT nội tại)**. ΔPSI > 0 nghĩa là đột biến **làm bền** peptide, tức vị trí đó thuộc degron.
- Hai nửa A/B là hai replicate: PSI tương quan **0,9544**, ΔPSI tương quan **0,8335**, nhiễu chiếm 16,7% phương sai. 235 peptide dựng được ma trận, **91** peptide còn lại sau ngưỡng degron PSI WT ≤ 3,0 ([pap-baseline](../research/pap-baseline/README.md)).
- **130** peptide có mặt ở cả hai bộ; phải nằm cùng một phía train/test.

**Bộ quét — đặc thù:**

- Mỗi peptide có `mut0` (hoang dã) và `mut1..mut28`, mỗi vị trí thay bằng **đúng một** amino acid theo quy tắc *opposite scanning*: `AGVLISTCDE → R`, `MWFP → S`, `YNQKRH → A`. Có 876 ngoại lệ ở vị trí 25–27.
- Nhãn đột biến: **ΔPSI = PSI(mutₖ) − PSI(mut0)**.
- **Footprint** (nhãn mức residue của bộ quét), định nghĩa trong `research/e3-labels-audit/count_footprints.py`: peptide là degron nếu PSI WT ≤ 3,0; cần ≥ 21/28 vị trí đạt `sum ≥ 10`; vị trí **thuộc footprint** nếu ΔPSI ≥ 1,0. Kết quả trên Replicate 1: 8.831 peptide → 3.439 degron → **2.624 có footprint** (2.402 khu trú ≤ 6 vị trí).
- `psi-wt.tsv` là **điều kiện khác** (nền BAG6 WT), không phải replicate thứ ba; không trộn ([full-data-audit §9](../research/full-data-audit/README.md)).

### 4.3 CSV gốc của tác giả: `I28 Scanning Mutagenesis Replicate 1.csv`

Nằm trong `interim/zhang-scanning-unzip/.../Replicate 1 (BAG6 genotype unclear)/`. Chỉ có cho Replicate 1; đây là căn cứ để kiểm `build_psi.py --validate`. 283.880 dòng (kể cả construct không có read).

| Cột | Ý nghĩa |
|---|---|
| (cột đầu, không tên) | Số thứ tự dòng do R ghi ra; bỏ qua |
| `Gene` | Định danh construct, cùng dạng `id` ở 4.1 |
| `DNA.Seq` | Trình tự DNA 84 nt mã hoá peptide, toàn chữ thường (không đánh dấu codon đột biến) |
| `AA.Seq` | Trình tự peptide 28 aa; residue bị đột biến viết **chữ thường**. Kết thúc bằng `*` nếu tile chạm đầu C protein (813 peptide chỉ có 27 aa) |
| `b1`..`b6` | **Read thô** ở bin 1..6 |
| `nb1`..`nb6` | Read chuẩn hoá, cùng công thức với 4.2 |
| `Sum` | `Σ nbᵢ` |
| `PSI` | Như 4.2; `NA` khi `Sum = 0` |

⚠ **Ba dòng sai do lỗi header của tác giả** (`A0A0B4J1Y8_IGLV9-49_1_mut{10,17,24}`): hai dòng đầu có `Sum = 0`/`PSI = NA` dù có read, dòng thứ ba lệch PSI 0,62. Các bảng `psi-*.tsv` đã sửa.

### 4.4 File đếm read gốc: `interim/zhang-*-unzip/**/LIB*_S<k>.txt`

Mỗi file là **một bin của một điều kiện**. Tab-separated, **không có header**, hai cột: `id` và số read thô (số nguyên). Thứ tự bin theo số `S<k>`: với bộ quét Replicate 1 và bộ bão hòa nửa A là `S1..S6` = bin 1..6; Replicate 2 và nửa B là `S7..S12` = bin 1..6. Ánh xạ đầy đủ từ file sang điều kiện nằm trong `CONDITIONS` của `research/full-data-audit/build_psi.py`.

## 5. Nhật ký xử lý

- **23/10/2026 — dọn repo:** Không đụng tới `data/`. Đã gỡ khỏi git (còn trong nhánh `backup-before-clean`): `research/{topic-decision.md, topic-argument-2026-10-15.md, contribution-assessment-2026-10-15.md, topic-report, cross-assay-model-2026-10-15, reframe-options-2026-10-15, experiment-report-2026-10-18, slide-example-2026-10-15}`, `lectures/{cs535, assets}`. Các mục nhật ký bên dưới nhắc tới script trong những thư mục này (ví dụ `reframe-options/method_debt.py`) chỉ còn là lịch sử; file dữ liệu chúng từng đọc/ghi không đổi. Kết quả Kaggle R0–R3 đặt ở `research/r*/run-kaggle-20261022/`.
- **23/10/2026 — R6 đã chạy trên Kaggle (kết quả):** Không tải dữ liệu mới, **không ghi/sửa gì trong `data/`**. Kết quả (JSON) ở `research/r6-ladder-scan-2026-10-23/run-kaggle-20261023/`, OOF `.npz` chỉ nằm trong `r6-results.zip` (không lên git); `posthoc_r6.py` đọc `data/processed/r6-scantable.npz` và cache bão hòa để đếm scanning ngoài mọi cụm bão hòa (4.441 peptide / 2.779 cụm / 123.718 ô, `posthoc-r6.json`), không ghi file dữ liệu. [Báo cáo](../research/r6-ladder-scan-2026-10-23/README.md) mục 3.
- **23/10/2026 — R6 (một notebook: ngữ cảnh rộng, scanning, ESM-2 bốn cỡ, CNN/mCNN; chưa chạy trên Kaggle):** Không tải dữ liệu mới, không sửa bảng/cụm cũ, **chưa huấn luyện mô hình thật**. **GHI MỚI:** `processed/r6-scantable.npz` (mục 3.3) và `processed/packages/degron-data-v2.zip` + `degron-code-f76ab5991b1f-dirty.zip` (gói để Trọng tự upload; v2 = v1 + file R6). Phép kiểm chéo mô tả scanning–bão hòa trên ô trùng (42/88/117 peptide): Pearson 0,79/0,74/0,70, κ 0,75/0,69/0,65, thang PSI(WT) hai nguồn lệch −0,01…+0,13 — **đính chính** diễn giải ở `r3-domain-gate/README.md`: độ lệch ≈ 0,9 là giữa sàng peptidome GPS và cả hai nguồn kia. [Báo cáo](../research/r6-ladder-scan-2026-10-23/README.md). Chỉ nguồn CC BY 4.0 (Zhang 2023) và mô hình ESM-2 (MIT, tải lúc chạy, không lưu trong repo).
- **22/10/2026 — hạ tầng notebook, R0 và R3 (cục bộ, không huấn luyện, không upload):** Không tải gì mới, không sửa bảng/cụm cũ. **GHI MỚI:** `interim/protein-id30-cov80-proteome_cluster.tsv` (phân cụm toàn proteome; phát hiện: cụm cũ chỉ có 6.573/18.753 protein của sàng peptidome), `processed/r3-sat-wt-pool.tsv`, `processed/packages/*` (gói upload; mục 3.3). Đo cục bộ nhẹ trên sàng peptidome: tile trùng định danh 235/235 peptide bão hòa, PSI tương quan 0,84 nhưng **lệch hằng số ≈ 0,9** giữa PSI sàng và PSI(WT) nội tại, sàng phủ 72,1% tile 28-mer proteome ([báo cáo](../research/r3-domain-gate-2026-10-22/README.md)). Notebook: [R0](../research/r0-reproduce-notebook-2026-10-22/README.md), [R3](../research/r3-domain-gate-2026-10-22/README.md); hướng dẫn chạy: [RUN.md](../research/notebook-kit-2026-10-22/RUN.md).
- **22/10/2026 — chuẩn bị dữ liệu cho R1/R2 (notebook GPU):** Không tải gì mới, không sửa bảng/cụm cũ, **chưa huấn luyện gì**. **GHI MỚI vào `data/processed/`** (cả hai gitignore, sinh lại được, mục 3.3): `r12-seqtable.npz` (trình tự WT/mutant, vị trí, acid amin của 92.337 ô của tập nới ngưỡng 4,0, đúng thứ tự gộp của `run_curve.py`; dựng bằng `research/r2-esm-features-2026-10-22/make_seqtable.py`, đã kiểm khớp nhãn và 600 hàng đặc trưng với hai cache learning-curve) và `r1-row-exclusion.npz` (mặt nạ loại hàng của bảng huấn luyện Degformer 569.270 dòng cho 5 outer fold + nhóm validation theo protein; dựng bằng `research/r1-degformer-clean-2026-10-22/build_exclusion_r1.py`, MMseqs2 2 luồng; hợp ba luật E1/E2/E3, loại 3,38–8,11% dòng mỗi fold, 99,83% dòng ánh xạ được vào UniProt người ghim; đếm ở [exclusion-summary.json](../research/r1-degformer-clean-2026-10-22/exclusion-summary.json)). Hai file là đầu vào của gói dữ liệu `degron-data-v1` cho R1 và R2 (khai trong `data-needs.json` từng thí nghiệm); giấy phép phái sinh: CC BY 4.0 (từ Zhang/UniProt) và Apache-2.0 (từ bảng huấn luyện của Degformer). [R1](../research/r1-degformer-clean-2026-10-22/README.md), [R2](../research/r2-esm-features-2026-10-22/README.md).
- **22/10/2026 — Koren 2018 (tải tay) và audit cổng P2:** Người dùng tải tay `supplement-{10..15}.xlsx` + `nihms967427.pdf` bằng trình duyệt; sao sang `raw/koren-2018/` kèm SHA-256 (mục 2). **GHI MỚI:** `interim/koren-2018-cells.tsv`, `interim/koren-2018-cluster/` (cả hai xoá được, dựng lại bằng `research/koren-s4-audit-2026-10-22/audit.py`). Không sửa bảng/cụm cũ. Ánh xạ file→bảng **đã xác nhận bằng cách mở file** (S4 = `supplement-11`). PSI tái tính khớp 1.827/1.827 dòng, nhưng thang **3 bin** (PSI ∈ [1;3]) khác thang 6 bin của Zhang, peptide 23-mer đầu C có codon dừng, chỉ 9 substrate → **5 cụm cov80 mới, cổng P2 không đạt**; vai trò còn lại: tập kiểm chứng ngoài. Giấy phép: không mở, chỉ dùng nội bộ. [Báo cáo](../research/koren-s4-audit-2026-10-22/README.md).
- **22/10/2026 — hiệu chuẩn P6 và nguyên mẫu G3:** Không tải gì mới. **GHI MỚI vào `data/processed/`:** ba file `calibration-p6-{oof,model,trainpath}.npz` (mục 3.3). Thêm `research/calibration-p6-2026-10-22/` (`PROTOCOL.md` chốt trước, `run_calibration.py`, `build_model.py`, `predict.py`, `verify.py`). Điểm thô tái tạo **khớp** `results.json` của P0 ở cả ba seed (sai lệch < 1e-9). Nguyên mẫu `predict.py` tái tính khớp đường huấn luyện và 15 mô hình fold với chênh tối đa < 1e-9. [Báo cáo](../research/calibration-p6-2026-10-22/README.md).
- **22/10/2026 — tiền huấn luyện P3:** Không tải gì mới, không sửa bảng/cụm cũ. **GHI MỚI vào `data/processed/`:** `p3-tile-exclusion.json`, `p3-progress.pkl`, `p3-pretrained/*.pt` (mục 3.3). Đọc tile Voutsinos (`degrons.csv.gz`, MIT) làm nhãn tiền huấn luyện, loại cả gene chạm cụm outer-test từng fold trước mọi bước học. [Báo cáo](../research/pretrain-p3-2026-10-22/README.md), tiền đăng ký ở `PROTOCOL.md` cùng thư mục.
- **22/10/2026 — đường cong học:** Không tải gì mới, không sửa bảng/cụm cũ. **GHI MỚI vào `data/`:** hai cache `processed/learning-curve-sat-{base,ext4.0}.npz` (mục 3.3). Thêm `research/learning-curve-2026-10-22/run_curve.py` (tiền đăng ký ở `PROTOCOL.md`) và `research/next-steps-plan-2026-10-22/{check_candidate_access.py,sat_filter_dropoff.py}` (chỉ đọc). Đếm được: trong **248** peptide bão hòa thô, **144** bị loại chỉ bởi ngưỡng `DEGRON_PSI_MAX = 3,0`, 13 vì lý do kỹ thuật; nới ngưỡng lên **4,0** thêm **85 peptide / 44.490 ô / 83 cụm cov80 mới**, tỉ lệ ô dương nhóm mới **0,1140** so với **0,1310** của nhóm gốc. Phép chia outer tái lập **trùng khớp** `folds` của G2, và ridge mức 100% cho đúng **0,8082**. Kết quả: ridge **0,8208** và `gate_no_pap` **0,8154** khi thêm nhãn nới ngưỡng vào *chỉ* outer-train, cùng outer-test 91 peptide. Phần B (tiền đăng ký riêng ở `PROTOCOL-B.md`) giữ phần cũ ở 100% và chỉ thay tỉ lệ cụm mới; không sinh file dữ liệu nào, đọc lại đúng hai cache trên. Phần C (`PROTOCOL-C.md`) chạy **cả bốn** ngưỡng 3,5/4,0/4,5/5,0 trong một lượt cùng ba `RESCUE_DELTA` và phân cụm cov50, sinh thêm ba cache `ext{3.5,4.5,5.0}`; lợi ích đạt đỉnh ở **4,0** (+0,0126) rồi suy giảm, và bền qua mọi điều kiện đã kiểm. ⚠ Ghi lại một điều: trên bộ 91 peptide (và trên base + 85 peptide của ngưỡng 4,0), **cov50 và cov80 cho cùng một phân hoạch**, nên dòng cov50 là phép kiểm chia lại fold, không phải kiểm độ mịn phân cụm. Cuối phiên thử truy cập supplementary Koren 2018 theo thứ tự quyền-trước-dữ-liệu: **không lấy được file**, và nguồn **không có giấy phép mở** — chi tiết ở mục 2 và [raw/koren-2018-probe/SOURCE.md](raw/koren-2018-probe/SOURCE.md). [Báo cáo thí nghiệm](../research/learning-curve-2026-10-22/README.md), [kế hoạch và khảo sát nguồn](../research/next-steps-plan-2026-10-22/README.md).
- **22/10/2026 — phân cụm lại (độ nhạy độ mịn):** Không tải gì mới. **GHI MỚI vào `data/`:** thư mục `interim/recluster-sensitivity/` (32 MB, gitignore, sinh lại được) gồm bốn phân hoạch MMseqs2 (`protein-id{20,10,10,00}-cov{50,50,30,30}_cluster.tsv` + log, `*_all_seqs.fasta`, `*_rep_seq.fasta`) trên cùng đầu vào `processed/proteins-full.fasta` (6.573 protein) và cùng cờ như bản gốc, chỉ đổi `--min-seq-id`/`-c`; SHA-256 từng tệp trong [cluster-manifest.json](../research/recluster-sensitivity-2026-10-22/cluster-manifest.json). Trên 176 peptide chỉ có **ba** phân hoạch khác phân hoạch cov80 (hạ identity dưới 0,2 không đổi nhóm nào). Lợi ích P0 giữ CI > 0 và ba seed dương ở cả ba (+0,0113…+0,0166). [Báo cáo](../research/recluster-sensitivity-2026-10-22/README.md).

- **21/10/2026 — MetaDegron:** tạo riêng `raw/metadegron/`; clone commit `ca12c0cf…`, tải toàn văn/supplementary qua PMC/Europe PMC, trang web mẫu và nguồn ELM. `fetch-sources.py` ghi truy cập; `audit_dataset.py` đếm schema/nhãn, dựng bảng chuỗi chỉ dưới raw/derived, phân cụm protein id30 cov50/cov80 và kiểm overlap với Zhang/Voutsinos/Larsen; `safe-predict-x.py` đọc literal cây số an toàn để tái tính nhánh X, không `pickle.load`, không chạy notebook/mã nguồn tải về; `review-labels.py` tổng hợp mẫu truy nguồn; `inventory-sources.py` ghi SHA-256 và giấy phép; `validate.py` kiểm chéo. Không gửi chuỗi lên server, không tải đủ checkpoint SeqVec/embedding lớn, không nhập nhãn binary vào ΔPSI, không sửa các bảng/cụm G2 cũ. Kết quả và giới hạn: [metadegron-analysis-2026-10-21](../research/metadegron-analysis-2026-10-21/README.md).

- **18/10/2026 (phiên sau)** — Không tải gì thêm. Sinh thêm dự đoán OOF và checkpoint cho ba thí nghiệm mở rộng (`g2-ext-*`), đọc lại cache bão hoà và nguồn Degformer đã ghim. [Báo cáo](../research/g2-extension-2026-10-18/README.md).
- **18/10/2026** — Tải Degformer ghim commit và kiểm SHA; tạo cache đặc trưng bão hòa, 45 checkpoint mạng và dự đoán OOF 3 seed ×5 fold; audit 42.163 sequence ô test trong training_data.csv. Script/lineage/schema ở mục 3; [báo cáo](../research/g2-saturation-2026-10-18/README.md).


Mới nhất ở trên. Chi tiết phân tích nằm trong báo cáo được dẫn; ở đây chỉ ghi việc gì đã làm **với dữ liệu**.

- **15/10/2026 (phiên 10)** — **TẢI MỚI:** ClinVar `variant_summary.txt.gz` vào `raw/clinvar/` (**455.785.525 byte**, SHA-256 `a5198a11…28218`, `Last-Modified` 12/10/2026). Sổ xuất xứ: [raw/clinvar/SOURCE.md](raw/clinvar/SOURCE.md). ⚠ **Không có số phiên bản, file bị ghi đè mỗi tuần** ⇒ muốn tái lập đúng số phải dùng `archive/variant_summary_2026-10.txt.gz`. ⚠ ClinVar **không phát hành kèm giấy phép kiểu CC**: chỉ có **yêu cầu ghi công** và một câu phủ nhận chẩn đoán phải đi theo đầu ra của ứng dụng — nguyên văn ở SOURCE.md mục 2. **GHI MỚI vào `data/`:** cache `interim/gps-peptidome-rep1.tsv` (475.506 dòng) và hai bảng `processed/clinvar-{scan-hits,driver-variants}.json`. Thêm hai script trong `research/variant-coverage-2026-10-15/`: `coverage.py` (bảy tầng độ phủ) và `enrichment.py` (Mantel–Haenszel). Đếm được: **116.702** tile degron / **17.287** protein ở ngưỡng PSI ≤ 3,0 (**32,4%** tile toàn proteome), **87,3%** cụm cov80 chưa thấy; ClinVar **2.564.486** missense, khớp toạ độ UniProt **93,0%**; **≈1.600** biến thể chấm được bằng đúng ô đã đo; tỉ số chênh gây bệnh/lành tính trong degron **2,148** (MH theo protein). Ba tầng cũ tái lập đúng phiên 8 (91 / 2.994 / 83.446 ô). Báo cáo: [variant-coverage](../research/variant-coverage-2026-10-15/README.md).
- **15/10/2026 (phiên 8)** — Không tải, không xử lý, **không ghi gì vào `data/`**. Thêm hai script **chỉ đọc** trong `research/residue-task-derisk-2026-10-15/`: `residue_data.py` (nạp hai nguồn nhãn mức residue) và `derisk.py` (sáu lệnh con). Đầu vào đã có: `processed/psi-{rep1,rep2,sat_a,sat_b}.tsv`, `interim/zhang-scanning-unzip/.../I28 Scanning Mutagenesis Replicate 1.csv`, `raw/human-reviewed-2026-10-12.fasta.gz`, `interim/protein-id30-cov80_cluster.tsv`, `interim/pap-weights/pap_weights/*.h5`. Đếm được: bộ quét **2.994 peptide degron / 1.985 cụm cov80 / 83.446 ô**, trần đo lường AUROC **0,9458**; bộ bão hòa **91 / 89 / 47.847**, trần **0,9519**, ICC ô-trong-peptide 0,0625. Kiểm chéo: n = 91, trần 0,9519 và ΔPAP `cnn2w1` **0,7693** tái lập đúng [pap-baseline §C](../research/pap-baseline/README.md). ⚠ Ghi lại một điều về `processed/psi-wt.tsv`: **không** dùng nó làm mốc WT cho bộ bão hòa (đó là quét BAG6 WT, D-028 mục 5 cấm trộn); mốc đúng là **WT nội tại** = trung vị ô đồng nghĩa, và chỉ cách đó mới tái lập được n = 91. Báo cáo: [residue-task-derisk](../research/residue-task-derisk-2026-10-15/README.md).
- **15/10/2026 (tối, phiên 6)** — **TẢI MỚI:** bộ nhân Larsen 2025 vào `raw/larsen-2025/` theo C-10, D-028 mục 6. `git clone` tag **`v1.0`** (commit `2698ecc6`), copy `annotations/transfac_tiles.csv.gz` (**5.771.779 byte**, SHA-256 `0c31057d…a2a2f`, **63.258 dòng**) và `LICENSE`. Sổ xuất xứ đầy đủ: [raw/larsen-2025/SOURCE.md](raw/larsen-2025/SOURCE.md). Audit khi tải: **59.016** tile có điểm trên **1.627** gene; độ tin cậy `degron_score` **0,9701** (trần r 0,9849); **Pearson(`pap`, `degron_score`) = −0,7899**, tái lập mốc 0,79 của tác giả; rASA có **phương sai thật** (trung vị 0,6900, SD 0,2334, **49,4%** tile > 0,7) — khác hẳn tập huấn luyện chính. ⚠ Số 63.258 **không khớp con số nào in trong bài** (58.781/58.992/62.992/63.011/63.230) ⇒ dùng số đếm được từ file.
- **15/10/2026 (tối, phiên 5)** — Vẫn **không ghi gì vào `data/`**. Thêm `research/reframe-options-2026-10-15/method_debt.py` (chỉ đọc, cùng ba đầu vào) → ba mô hình cho bậc thang cụm/assay và bootstrap ×40 cho độ ổn định trọng số. Báo cáo: reframe-options §11.
- **15/10/2026 (tối, phiên 3–4)** — Vẫn **không ghi gì vào `data/`**. Thêm `research/reframe-options-2026-10-15/cascade_and_offset.py` (chỉ đọc) trên cùng ba đầu vào như `cross_assay_gap.py` → đối chứng offset (biến thiên 0,0044 AUROC) và bậc thang 2×2 trên 5 seed (dịch chuyển cụm −0,0039 so với dịch chuyển assay +0,1061). Báo cáo: reframe-options §10.
- **15/10/2026 (tối)** — Không tải, không xử lý, **không ghi gì vào `data/`**. Hai phân tích **chỉ đọc** được chạy trên dữ liệu đã có, kết quả nằm trong `research/`:
  - `research/reframe-options-2026-10-15/probe_tile_reliability.py` đọc `raw/voutsinos-2026/repo/score/degrons.csv.gz` → độ tin cậy từ cột sai số từng tile (212.658 tile / 5.327 gene; `degron_score` 0,9807, `abundance_score` 0,8549; hai cột tương quan −0,9558).
  - `research/reframe-options-2026-10-15/cross_assay_gap.py` đọc `interim/zhang-gps-unzip/.../Machine Learning Prediction of I28 Peptidome PSI (Complete Coverage & 10% Training).csv`, `raw/voutsinos-2026/repo/score/degrons.csv.gz` và `interim/protein-id30-cov80_cluster.tsv` → 17.820 trình tự 28-mer dùng chung hai assay, 4.610 accession, 4.308 cụm cov80; khoảng cách qua assay 0,0773 AUROC. Báo cáo: reframe-options §9.
- **15/10/2026** — Không tải gì mới. Kiểm giấy phép bộ nhân Larsen 2025 (MIT qua GitHub) và repo Degformer (Apache-2.0), **chưa tải** cả hai. Viết file này, kèm giải thích các trường của tập huấn luyện chính (mục 4); đối chiếu SHA-256 xác nhận `interim/scanning-replicate-1.csv` và `processed/footprint-rerun.json` là bản thừa.
- **14/10/2026** — Tải 8 cấu trúc AlphaFold v6 vào `raw/alphafold/`. Giải nén trọng số PAP vào `interim/pap-weights/`. Tái lập PAP khớp bốn chữ số với số công bố. Báo cáo: [pap-baseline](../research/pap-baseline/README.md), [architecture-check](../research/architecture-check/README.md).
- **13/10/2026** — `fetch_all.py` tải đủ 4 nguồn (Mendeley 5/5 file, GEO, Voutsinos @ `9b3eafa6`, MaveDB 26 set), ghi `full-download-manifest.json`. Giải nén ba ZIP Zhang vào `interim/`. `build_psi.py` dựng PSI cho 5 điều kiện; phát hiện **lỗi header trong pipeline của Zhang** (mất dòng đầu mỗi file count → 3 id `A0A0B4J1Y8_IGLV9-49_1_mut{10,17,24}` sai trong CSV công bố); `--validate` mô phỏng lỗi để khớp số tác giả, còn bảng xuất ra đã sửa. Báo cáo: [full-data-audit](../research/full-data-audit/README.md).
- **12/10/2026** — `fetch_scanning.py` tải 2 ZIP quét/bão hòa. `audit_composition.py` tạo `composition-peptides.csv`, `protein-accessions.txt`. `prepare_protein_clusters.py` tải snapshot Swiss-Prot 2026_03 + 17 accession bổ sung, dựng `proteins-full.fasta`, chạy MMseqs2 ở coverage 0,8 và 0,5. Dữ liệu chuyển từ `data/` ở gốc repo vào thư mục đề tài cùng ngày. Báo cáo: [e3-labels-audit](../research/e3-labels-audit/README.md), [composition-context-audit](../research/composition-context-audit.md).
- **11/10/2026** — Phân tích đầu tiên ([voutsinos-2026-audit](../research/voutsinos-2026-audit/README.md), [e3-labels-audit](../research/e3-labels-audit/README.md)) chạy trên file tải vào thư mục tạm, không còn lưu ở đây.

## 6. Dựng lại từ đầu

```bash
# 1. Tải (Mendeley, GEO, Voutsinos, MaveDB) + kiểm SHA-256 + ghi manifest
.venv/bin/python topics/degron-footprint/research/full-data-audit/fetch_all.py

# 2. Giải nén
cd topics/degron-footprint/data
mkdir -p interim/zhang-scanning-unzip interim/zhang-saturation-unzip interim/zhang-gps-unzip interim/pap-weights
unzip -oq "raw/I28 Scanning Mutagenesis.zip" -d interim/zhang-scanning-unzip
unzip -oq "raw/I28 CRL Saturation Mutagenesis.zip" -d interim/zhang-saturation-unzip
unzip -oq "raw/I28 GPS Peptidome Screen and MLN4924 and SVM.zip" -x "*.xlsx" -d interim/zhang-gps-unzip
tar -xzf raw/voutsinos-2026/repo/models/pap_weights.tgz -C interim/pap-weights
cd ../../..

# 3. Bảng PSI (có cổng kiểm; lệch quá ngưỡng thì dừng, không ghi)
.venv/bin/python topics/degron-footprint/research/full-data-audit/build_psi.py --condition all --validate

# 4. Bảng thành phần + danh sách accession, rồi trình tự + cụm protein (cần mmseqs trong PATH)
.venv/bin/python topics/degron-footprint/research/e3-labels-audit/audit_composition.py
.venv/bin/python topics/degron-footprint/research/e3-labels-audit/prepare_protein_clusters.py --coverage 0.8
.venv/bin/python topics/degron-footprint/research/e3-labels-audit/prepare_protein_clusters.py --coverage 0.5

# 5. Cấu trúc AlphaFold (cần User-Agent)
cd topics/degron-footprint/data/raw/alphafold
for a in P60484 P51580 Q9NV35 P45381 O60260 P35557 P11712 P33261; do
  curl -s -A "Mozilla/5.0" -o AF-$a-F1-model_v6.pdb https://alphafold.ebi.ac.uk/files/AF-$a-F1-model_v6.pdb
done
sha256sum -c <(awk '{print $3"  AF-"$1"-F1-model_v6.pdb"}' manifest.txt)
```

Snapshot UniProt dùng nhãn `--date 2026-10-12`; tải lại hôm khác sẽ ra release khác và **SHA-256 không khớp**, script dừng. Muốn giữ đúng số liệu cũ thì giữ file `.fasta.gz` hiện có.

## 7. Lưu ý khi dùng

- **Thang PSI của Zhang: 1..6, thấp = bị phân hủy nhanh.** Bộ nhân Larsen (nếu tải) dùng thang **đảo chiều** và chuẩn hoá lại; không trộn trực tiếp.
- **Không trộn mẫu BAG6 WT (`psi-wt.tsv`) với hai replicate** — ΔPSI chỉ tương quan 0,56–0,58 và lệch hệ thống −0,11 PSI ([full-data-audit §9](../research/full-data-audit/README.md)).
- **Rò rỉ chéo:** 725/770 peptide footprint có tile trong tập train của PAP (`models/degron_train.csv.gz`); ghi vào thiết kế benchmark.
- **Ghi công khi dùng lại:** CC BY 4.0 (Mendeley, UniProt, AlphaFold) và MIT (Voutsinos) đều đòi ghi nguồn; trích DOI/URL ở mục 2.
