# Dữ liệu của đề tài `degron-footprint` — nguồn gốc và quá trình xử lý

> File này là **sổ nguồn gốc** của thư mục `data/`: mỗi file đến từ đâu, phiên bản nào, giấy phép gì, ai/script nào tạo ra, và đã xử lý qua những bước nào. Nội dung `data/` bị `.gitignore` chặn; **riêng file này được lên git** (ngoại lệ `!**/data/README.md`).
>
> Cập nhật lần cuối: **15/10/2026**. Tổng dung lượng ≈ 1,9 GB (`raw/` 694 MB · `interim/` 1,1 GB · `processed/` 117 MB).
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
| 1 | **Zhang et al. 2023**, *Molecular Cell* — đột biến quét, bão hòa, sàng peptidome GPS, CRISPR. [Ghi chép bài](../../../lectures/degron-basics/papers/zhang-2023.md) | Mendeley Data [`10.17632/32h94v2yv2.2`](https://data.mendeley.com/datasets/32h94v2yv2/2) (phiên bản 2), cả 5 file | **CC BY 4.0** (dữ liệu); bài báo All rights reserved | 12/10 (2 file), 13/10 (đủ 5) | `raw/*.zip`, `raw/Zhang et al., Raw Image Data Compiled.pdf` | SHA-256 **khớp checksum Mendeley công bố** — `raw/full-download-manifest.json` → `mendeley` |
| 2 | **Zhang et al. 2023** — bảng PSI peptidome | NCBI GEO [`GSE240610`](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE240610): Table S1 + `GSE240610_RAW.tar` (60 file count) + `filelist.txt` | Theo điều khoản GEO (công khai) | 13/10 | `raw/geo-gse240610/` | GEO không công bố checksum; SHA-256 ghi lúc tải — manifest → `geo` |
| 3 | **Voutsinos et al. 2026**, *Science Advances* ([DOI 10.1126/sciadv.adz3483](https://doi.org/10.1126/sciadv.adz3483)) — thư viện tile bào tương, điểm degron, mô hình PAP. [Ghi chép bài](../../../lectures/degron-basics/papers/voutsinos-2026.md) | GitHub [`KULL-Centre/_2025_Voutsinos_degron_cytosol`](https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol) @ **`9b3eafa6bd9730c558cd018063fa0180edf9db1a`** (main, 06/03/2026) | **MIT** (mã + dữ liệu trong repo); bài báo CC BY-NC 4.0 | 13/10 | `raw/voutsinos-2026/repo/` (50 file) | Kiểm `HEAD` đúng commit ghim; SHA-256 từng file — manifest → `voutsinos`. **Zenodo `16925278` trả 403 từ mạng này**, nên dùng repo GitHub cùng tác giả |
| 4 | **MaveDB** — 26 score set của 9 gene trong bài Voutsinos (PTEN, TPMT, NUDT15, CYP2C9, CYP2C19, ASPA, PRKN, GCK, LDLR). [Ghi chép](../../../lectures/degron-basics/papers/mavedb.md) | API `api.mavedb.org/api/v1`, URN từng score set trong `raw/mavedb/score-sets.json` | **CC0** (cả 26 set, đọc từ metadata) | 13/10 | `raw/mavedb/` | MaveDB có thể cập nhật; SHA-256 ghi lúc tải — manifest → `mavedb` |
| 5 | **UniProtKB/Swiss-Prot** người (snapshot) | `rest.uniprot.org/uniprotkb/stream`, truy vấn `(organism_id:9606) AND (reviewed:true)`, **release 2026_03** | CC BY 4.0 | 12/10 | `raw/human-reviewed-2026-10-12.fasta.gz` | SHA-256 trong `raw/human-reviewed-2026-10-12.fasta.manifest.json`, script kiểm lại mỗi lần chạy |
| 6 | **UniProtKB** — 17 accession không có trong snapshot (đã đổi tên/gộp/rút) | `rest.uniprot.org/uniprotkb/<acc>.fasta`, ghi cả URL sau redirect | CC BY 4.0 | 12/10 | `raw/uniprot-additional/` | SHA-256 trong `raw/uniprot-additional/manifest.json` |
| 7 | **AlphaFold DB v6** — 8 cấu trúc protein MaveDB | `alphafold.ebi.ac.uk/files/AF-<acc>-F1-model_v6.pdb` (**cần User-Agent**, nếu không EBI trả 403) | CC BY 4.0 | 14/10 | `raw/alphafold/` | Số residue + SHA-256 trong `raw/alphafold/manifest.txt` |

**Chưa tải (không có trong `data/`):** read giải trình tự thô (SRA `PRJNA1277273` của Zhang); bộ nhân Larsen 2025 (chờ [C-10](../../../DECISIONS.md), đường tải và giấy phép ở [resources/README.md §4](../../../resources/README.md)); repo Degformer (chờ [C-11](../../../DECISIONS.md), checkpoint là pickle — phải để thư mục biệt lập).

## 3. Danh mục từng file

### 3.1 `raw/`

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

### 3.3 `processed/`

| File | Sinh bởi | Đầu vào | Ghi chú / kiểm |
|---|---|---|---|
| `psi-rep1.tsv` (261.868 id), `psi-rep2.tsv` (261.999), `psi-wt.tsv` (264.036) | `research/full-data-audit/build_psi.py --condition all --validate` (13/10) | `interim/zhang-scanning-unzip/` | Cột `id psi sum nb1..nb6`. **Cổng kiểm:** dựng lại PSI Replicate 1 từ count thô và so với CSV tác giả, lệch lớn nhất **5,0 × 10⁻⁷** trên 261.865 giá trị → đạt (`research/full-data-audit/psi-build.json`) |
| `psi-sat_a.tsv` (134.608), `psi-sat_b.tsv` (134.563) | như trên | `interim/zhang-saturation-unzip/` | `sat_a` = file S1–S6, `sat_b` = S7–S12; giả định hai nửa là hai replicate đã kiểm bằng tương quan PSI **0,9544** |
| `composition-peptides.csv` | `research/e3-labels-audit/audit_composition.py` (12/10) | `raw/I28 Scanning Mutagenesis.zip` (đọc thẳng từ ZIP) | Chỉ số theo peptide, ngưỡng reads ≥ 10 |
| `protein-accessions.txt` (6.582 accession) | như trên | như trên | Đầu vào của `prepare_protein_clusters.py` |
| `proteins-full.fasta` (6.573 protein) | `prepare_protein_clusters.py` (12/10) | `raw/human-reviewed-*.fasta.gz` + `raw/uniprot-additional/` | Trình tự **hiện hành** của UniProt, không phải bản lịch sử lúc dựng thư viện. 9 accession thiếu được **loại**, không gán cụm riêng |
| `proteins-reviewed.fasta` (6.565), `missing-reviewed-accessions.txt` (17) | Phiên 12/10, **bản sớm hơn** của bước lấy trình tự; không còn script nào trong repo tạo ra | snapshot Swiss-Prot | Đã kiểm: mọi trình tự trùng với `proteins-full.fasta`. Bản lịch sử, bị thay bởi `proteins-full.fasta` |
| `footprint-rerun.json` | `research/e3-labels-audit/count_footprints.py` (chạy lại 12/10) | CSV Replicate 1 | **Trùng byte** với `research/e3-labels-audit/footprint-audit.json` (2.624 footprint). Bản thừa |

## 4. Các trường của tập huấn luyện chính

Theo [D-025](../../../DECISIONS.md#d-025), nhãn chính lấy từ **bộ bão hòa** (`psi-sat_a.tsv`, `psi-sat_b.tsv`), còn **bộ quét** (`psi-rep1.tsv`, `psi-rep2.tsv`) là nguồn phụ. Nhãn dùng là trung bình hai replicate. Cả hai bộ là **peptide 28-mer gắn vào đầu C của GFP** trong hệ GPS (Global Protein Stability) của Zhang 2023: tế bào được sort thành **6 bin** theo tỉ lệ GFP/DsRed, bin 1 là kém bền nhất, bin 6 là bền nhất. Peptide càng nằm ở bin thấp thì càng bị phân hủy nhanh.

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

Mới nhất ở trên. Chi tiết phân tích nằm trong báo cáo được dẫn; ở đây chỉ ghi việc gì đã làm **với dữ liệu**.

- **15/10/2026 (phiên 8)** — Không tải, không xử lý, **không ghi gì vào `data/`**. Thêm hai script **chỉ đọc** trong `research/residue-task-derisk-2026-10-15/`: `residue_data.py` (nạp hai nguồn nhãn mức residue) và `derisk.py` (sáu lệnh con). Đầu vào đã có: `processed/psi-{rep1,rep2,sat_a,sat_b}.tsv`, `interim/zhang-scanning-unzip/.../I28 Scanning Mutagenesis Replicate 1.csv`, `raw/human-reviewed-2026-10-12.fasta.gz`, `interim/protein-id30-cov80_cluster.tsv`, `interim/pap-weights/pap_weights/*.h5`. Đếm được: bộ quét **2.994 peptide degron / 1.985 cụm cov80 / 83.446 ô**, trần đo lường AUROC **0,9458**; bộ bão hòa **91 / 89 / 47.847**, trần **0,9519**, ICC ô-trong-peptide 0,0625. Kiểm chéo: n = 91, trần 0,9519 và ΔPAP `cnn2w1` **0,7693** tái lập đúng [pap-baseline §C](../research/pap-baseline/README.md). ⚠ Ghi lại một điều về `processed/psi-wt.tsv`: **không** dùng nó làm mốc WT cho bộ bão hòa (đó là quét BAG6 WT, [D-028](../../../DECISIONS.md#d-028) mục 5 cấm trộn); mốc đúng là **WT nội tại** = trung vị ô đồng nghĩa, và chỉ cách đó mới tái lập được n = 91. Báo cáo: [residue-task-derisk](../research/residue-task-derisk-2026-10-15/README.md).
- **15/10/2026 (tối, phiên 6)** — **TẢI MỚI:** bộ nhân Larsen 2025 vào `raw/larsen-2025/` theo [C-10, D-028 mục 6](../../../DECISIONS.md#d-028). `git clone` tag **`v1.0`** (commit `2698ecc6`), copy `annotations/transfac_tiles.csv.gz` (**5.771.779 byte**, SHA-256 `0c31057d…a2a2f`, **63.258 dòng**) và `LICENSE`. Sổ xuất xứ đầy đủ: [raw/larsen-2025/SOURCE.md](raw/larsen-2025/SOURCE.md). Audit khi tải: **59.016** tile có điểm trên **1.627** gene; độ tin cậy `degron_score` **0,9701** (trần r 0,9849); **Pearson(`pap`, `degron_score`) = −0,7899**, tái lập mốc 0,79 của tác giả; rASA có **phương sai thật** (trung vị 0,6900, SD 0,2334, **49,4%** tile > 0,7) — khác hẳn tập huấn luyện chính. ⚠ Số 63.258 **không khớp con số nào in trong bài** (58.781/58.992/62.992/63.011/63.230) ⇒ dùng số đếm được từ file.
- **15/10/2026 (tối, phiên 5)** — Vẫn **không ghi gì vào `data/`**. Thêm `research/reframe-options-2026-10-15/method_debt.py` (chỉ đọc, cùng ba đầu vào) → ba mô hình cho bậc thang cụm/assay và bootstrap ×40 cho độ ổn định trọng số. Báo cáo: [reframe-options §11](../research/reframe-options-2026-10-15/README.md).
- **15/10/2026 (tối, phiên 3–4)** — Vẫn **không ghi gì vào `data/`**. Thêm `research/reframe-options-2026-10-15/cascade_and_offset.py` (chỉ đọc) trên cùng ba đầu vào như `cross_assay_gap.py` → đối chứng offset (biến thiên 0,0044 AUROC) và bậc thang 2×2 trên 5 seed (dịch chuyển cụm −0,0039 so với dịch chuyển assay +0,1061). Báo cáo: [reframe-options §10](../research/reframe-options-2026-10-15/README.md).
- **15/10/2026 (tối)** — Không tải, không xử lý, **không ghi gì vào `data/`**. Hai phân tích **chỉ đọc** được chạy trên dữ liệu đã có, kết quả nằm trong `research/`:
  - `research/reframe-options-2026-10-15/probe_tile_reliability.py` đọc `raw/voutsinos-2026/repo/score/degrons.csv.gz` → độ tin cậy từ cột sai số từng tile (212.658 tile / 5.327 gene; `degron_score` 0,9807, `abundance_score` 0,8549; hai cột tương quan −0,9558).
  - `research/reframe-options-2026-10-15/cross_assay_gap.py` đọc `interim/zhang-gps-unzip/.../Machine Learning Prediction of I28 Peptidome PSI (Complete Coverage & 10% Training).csv`, `raw/voutsinos-2026/repo/score/degrons.csv.gz` và `interim/protein-id30-cov80_cluster.tsv` → 17.820 trình tự 28-mer dùng chung hai assay, 4.610 accession, 4.308 cụm cov80; khoảng cách qua assay 0,0773 AUROC. Báo cáo: [reframe-options §9](../research/reframe-options-2026-10-15/README.md).
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
