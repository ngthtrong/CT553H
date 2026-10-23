# Hướng dẫn tìm hiểu dữ liệu degron-footprint: từ phép đo đến tập học

Đối chiếu ngày **21/10/2026** với file dữ liệu đang có, code nạp dữ liệu và kết quả audit trong repo. Tài liệu dành cho người có nền tảng kỹ thuật phần mềm, mới học sinh học. Mục tiêu là đọc được một dòng dữ liệu, tự giải thích cách tạo nhãn và hiểu vì sao cách chia tập ảnh hưởng kết luận.

**Cách dùng:** đọc mục 1–5 để hiểu ý nghĩa; làm mục 6–8 để chạm dữ liệu; đọc mục 9–12 để hiểu đánh giá và tránh suy luận sai. Có thể chia thành hai buổi, mỗi buổi khoảng 2 giờ; thời lượng là gợi ý, không phải yêu cầu phải học xong trong một lần.

## 1. Những điểm được sửa so với bản hướng dẫn ban đầu

| Nội dung                                              | Cách hiểu sau đối chiếu                                                                                                                                                                                                         |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| “ΔPSI dương nghĩa là vị trí thuộc degron”    | Đột biến làm **reporter bền hơn** trong assay. ΔPSI ≥1 là tiêu chí vận hành để gọi ô dương; đây là bằng chứng về độ nhạy tại vị trí, chưa xác nhận trực tiếp E3 nhận diện residue đó.  |
| “Mô hình không thể vượt trần AUROC 0,9519”    | 0,9519 là AUROC dùng lần đo A chấm nhãn của lần B. Nó là mốc đồng thuận thực nghiệm, **không phải cận trên toán học**; nhãn G2 lại là trung bình A/B.                                                |
| “Nhiễu chiếm 16,7%”                                | Ước lượng từ phân tích ma trận rộng hơn, 235 peptide; không tự gán cho riêng 91 peptide G2 hoặc nhãn trung bình hai lần đo.                                                                                       |
| “Các bộ dùng chung ngưỡng ≥21 vị trí”        | Loader quét dùng ≥21 vị trí. Loader bão hòa yêu cầu ≥10 ô giữ nguyên amino acid ở **mỗi** nửa để lấy WT, giao ô hai nửa và các kiểm trình tự; không có điều kiện ≥21 vị trí trong hàm đó. |
| “2.624 footprint là tập quét mà loader trả về” | Đây là số theo phép đếm lịch sử có yêu cầu tồn tại vị trí dương. Loader hiện tại trả **2.994 peptide degron**, không bắt buộc có ô dương.                                                          |
| Ví dụ code “dựng ΔPSI”                           | Đoạn pivot PSI chỉ xem PSI; muốn có ΔPSI phải xác định trình tự WT, dựng WT riêng từng replicate, rồi trừ. Mục 7 làm đủ các bước này.                                                                       |
| Các liên kết bài học cũ                          | [Bài 2](02-how-degrons-are-measured.md) đang đảo chiều PSI/ΔPSI và mô tả vai trò dữ liệu cũ. Không dùng bảng chiều điểm trong bài đó để diễn giải Zhang.                                                    |
| “Kiểm tra ngoài” bằng MaveDB/ClinVar              | Đây là nguồn cho đối chiếu hoặc ứng dụng có điều kiện; có file không đồng nghĩa đã có tập test độc lập, cùng endpoint, không rò rỉ.                                                                    |

Nguồn quyết định kỹ thuật của hướng dẫn: [residue_data.py](../../topics/degron-footprint/research/residue-task-derisk-2026-10-15/residue_data.py), [derisk.py](../../topics/degron-footprint/research/residue-task-derisk-2026-10-15/derisk.py), [runner G2](../../topics/degron-footprint/research/g2-saturation-2026-10-18/run.py). Hướng dẫn này không sửa các tài liệu lịch sử được dẫn.

## 2. Trước hết: một mẫu dữ liệu là cái gì?

**Protein** là một chuỗi amino acid. **Residue** là một amino acid tại một vị trí trong chuỗi. **Peptide** là một đoạn chuỗi ngắn; trong dữ liệu Zhang đang dùng, thiết kế chính là đoạn 28 residue. **Tile** là một đoạn được cắt theo cửa sổ dọc protein. **WT**, viết tắt của wild type, là trình tự tham chiếu trước thay thế; WT không có nghĩa là không mang degron hoặc bền nhất.

**Degron** là tín hiệu trong protein có thể góp phần khiến hệ thống phân hủy nhận diện protein. Hoạt tính còn phụ thuộc bối cảnh tế bào và khả năng tiếp cận tín hiệu. Bài toán ở đây đo hiệu ứng trên peptide gắn vào reporter.

Ví dụ minh họa ngắn, không phải một dòng dữ liệu thật:

```text
WT:     M K T A L V A
Mutant: M K T V L V A
              ↑
           vị trí 4
```

`A4V` nghĩa là thay A tại vị trí 4 bằng V. Một đầu vào cần biết **trình tự WT + vị trí + amino acid thay vào**. Đầu ra mong muốn là ảnh hưởng của phép thay thế này lên điểm ổn định reporter.

Với peptide 28 residue:

- Bảng thiết kế có 28 × 20 = **560 ô** nếu tính cả ô giữ nguyên amino acid.
- Có 28 ô giữ nguyên amino acid, mỗi vị trí một ô.
- Còn 28 × 19 = **532 phép thay thế thật** tối đa.

Đây là ma trận **vị trí × amino acid thay vào**, không phải ma trận tương tác 28 × 28 giữa các cặp vị trí. Một vị trí có thể nhạy với thay thế A→R nhưng ít nhạy với A→V. Vì vậy nhãn của một ô và nhãn gộp cho một vị trí là hai đối tượng khác nhau.

## 3. Từ tế bào phát sáng đến PSI và ΔPSI

### 3.1 Vì sao đo ánh sáng?

Trong thiết kế Zhang được pipeline sử dụng, peptide gắn ở đầu C của GFP, một protein phát huỳnh quang xanh. DsRed là tín hiệu chuẩn. Tế bào được phân vào **6 bin** theo tỉ lệ GFP/DsRed; bin 1 tương ứng reporter kém bền, bin 6 tương ứng reporter bền hơn.

Nếu peptide thúc đẩy reporter bị phân hủy, tín hiệu GFP tương đối giảm. Đây là cách đo gián tiếp hoạt tính liên quan độ ổn định. **PSI không phải thời gian bán hủy tính bằng giờ**, và không phải xác suất gây bệnh.

### 3.2 Vì sao phải chuẩn hóa read trước khi tính điểm?

Sau phân loại tế bào và giải trình tự, mỗi construct có số read ở từng bin. Tổng số read giữa các bin có thể khác nhau. Nếu lấy trung bình trực tiếp từ count thô, bin được đọc sâu hơn có thể chi phối điểm.

Pipeline trong [build_psi.py](../../topics/degron-footprint/research/full-data-audit/build_psi.py) dùng:

```text
T_i      = tổng read của bin i trên các id được xét
factor_i = T_1 / T_i
nb_i     = b_i × factor_i
sum      = nb_1 + ... + nb_6
PSI      = (1×nb_1 + 2×nb_2 + ... + 6×nb_6) / sum
```

`b_i` là read thô; `nb_i` là read sau chuẩn hóa. Vì vậy cột `sum` trong bảng PSI có thể là số thực. Ngưỡng `sum ≥10` trong loader là ngưỡng trên **tổng sau chuẩn hóa**, không phải khẳng định có ít nhất 10 read thô.

Ví dụ tự đặt: `nb = [0, 50, 50, 0, 0, 0]` cho PSI = 2,5. Nếu tín hiệu dồn vào bin 5–6 thì PSI cao hơn.

**Chiều cần nhớ với Zhang: PSI thấp → reporter kém bền → hoạt tính degron mạnh hơn trong assay.** Các nguồn khác có thể dùng điểm đảo chiều hoặc thang khác; phải đọc định nghĩa riêng của từng nguồn.

### 3.3 ΔPSI trả lời câu hỏi nào?

```text
ΔPSI = PSI(mutant) − PSI(WT/reference)
```

Ví dụ tự đặt, PSI WT = 2,2:

| PSI mutant | ΔPSI | Diễn giải trong assay                                                                            |
| ---------: | ----: | -------------------------------------------------------------------------------------------------- |
|        3,7 |  +1,5 | Reporter bền hơn; phù hợp với đột biến làm giảm hoạt tính gây phân hủy của peptide |
|        2,3 |  +0,1 | Thay đổi nhỏ trên phép đo này                                                               |
|        1,5 | −0,7 | Reporter kém bền hơn                                                                            |

Ngưỡng nhị phân của benchmark là **ΔPSI ≥1**. Mô hình học giá trị ΔPSI liên tục; khi chấm AUROC, nhãn được chuyển thành dương/âm theo ngưỡng này. Ô âm vì chưa đạt ngưỡng không đồng nghĩa “chắc chắn không có tác động sinh học”.

Footprint là cách mô tả các vị trí nhạy đột biến theo một quy tắc cụ thể. Tín hiệu này chưa đủ kết luận vị trí tiếp xúc trực tiếp với E3, hành vi của protein nguyên vẹn hoặc ý nghĩa bệnh học của biến thể.

## 4. Bản đồ nguồn dữ liệu và vai trò

Sổ nguồn gốc nằm ở [data/README.md](../../topics/degron-footprint/data/README.md): nguồn tải, snapshot, giấy phép, SHA-256, file trung gian và nhật ký. Hãy xem đây là danh mục provenance; code loader cho biết chính xác tập nào được đưa vào phép đo hiện hành.

| Nguồn                      | Đơn vị nhãn                                                 | Quy mô trong hồ sơ repo                                              | Vai trò và giới hạn                                                                           |
| --------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Zhang bão hòa             | Một phép thay amino acid tại một vị trí                   | 249 peptide xuất hiện trong các bảng PSI; G2 dùng 91 peptide       | Nhãn chính của benchmark G2 hiện tại                                                         |
| Zhang quét                 | Một phép thay thế được thử tại mỗi vị trí            | Rep1 có 9.590 peptide trước lọc; loader trả 2.994                  | Nguồn bổ sung; không có đầy đủ 19 thay thế thật ở mỗi vị trí                        |
| Voutsinos 2026              | Một điểm cho cả tile                                        | 212.658 tile / 5.327 gene theo audit lưu                               | Nguồn mức đoạn, baseline PAP và hướng giám sát phụ; chưa tự tạo nhãn từng ô ΔPSI |
| Larsen 2025                 | Một điểm cho cả tile từ yếu tố phiên mã                | 59.016 tile có điểm theo audit lưu                                  | Khảo sát chuyển miền sang nhân; cần kiểm thang điểm và khác assay                      |
| Zhang CRISPR                | Quan hệ từ screen với thành phần E3                        | 31 screen / 10 E3 gán được; một E3 có ≥5 peptide                 | Ca nghiên cứu; không đủ cơ sở cho bài toán phân lớp E3 rộng                           |
| MaveDB                      | Điểm biến thể, endpoint tùy score set                      | 26 score set / 9 gene đã thu thập                                    | Phải kiểm từng assay, trình tự và overlap trước đối chiếu ngoài                       |
| ClinVar                     | Thông tin biến thể và diễn giải lâm sàng                | Snapshot cục bộ ghi trong sổ nguồn                                  | Khảo sát độ phủ/toạ độ; không dùng pathogenic/benign thay cho ΔPSI                     |
| MetaDegron                  | Nhãn degron/motif từ nguồn curate và tập mẫu đối chứng | Audit mới ghi 302 dòng curate / 240 accession                         | Đối chiếu motif/E3, không phải tập ΔPSI bão hòa                                          |
| UniProt, MMseqs2, AlphaFold | Trình tự, cụm, cấu trúc dự đoán                         | Snapshot trình tự, cụm cov80/cov50; 8 cấu trúc AlphaFold đã tải | Dữ liệu hỗ trợ; không tự cung cấp nhãn hiệu ứng đột biến                             |

Các quy mô ngoài Zhang ở bảng này là **đọc lại audit đã lưu**, không phải tải lại hoặc tái đếm toàn bộ nguồn trong lần viết hướng dẫn. Xem [nhật ký nguồn](../../topics/degron-footprint/data/README.md#5-nhật-ký-xử-lý) và [audit MetaDegron](../../topics/degron-footprint/research/metadegron-analysis-2026-10-21/README.md).

Trong ngữ cảnh học đa mức, “nhãn yếu mức đoạn” chỉ là nhãn không xác định từng vị trí/thay thế; không có nghĩa phép đo toàn đoạn kém chất lượng.

### Cấu trúc thư mục

```text
topics/degron-footprint/
  data/raw/         nguồn tải, snapshot và hồ sơ nguồn
  data/interim/     file giải nén, trình tự/cụm và nguyên liệu trung gian
  data/processed/   bảng PSI, cache đặc trưng, dự đoán đã xử lý
  research/         code xử lý, protocol, audit và báo cáo kết quả
```

`processed` không có nghĩa đã đủ sạch cho mọi mục đích. Ví dụ bảng PSI vẫn chứa ô dưới ngưỡng độ sâu; loader mới thực hiện lọc cho bài toán cụ thể.

## 5. Đọc tên id và nội dung file

### 5.1 Một id mã hóa những gì?

```text
A2RUQ5_C17orf102_2_mut10a
│      │         │    │ └─ thay vào A (chữ thường trong id)
│      │         │    └── vị trí 10 trong peptide
│      │         └─────── tile số 2
│      └───────────────── gene
└──────────────────────── accession UniProt
```

Phần trước `_mut` là id peptide. Quét dùng dạng `..._mut10` và có `..._mut0` cho WT. Bão hòa dùng dạng `..._mut10a`, không có `_mut0` riêng.

Quy tắc tile: bắt đầu tại residue **(n−1)×23+1** trong cách đánh số sinh học từ 1. Trong Python dùng `protein[(n-1)*23:(n-1)*23+28]`. Hai tile liền nhau chồng 5 residue.

Ví dụ tile 2 bắt đầu tại residue 24; vị trí 10 của tile tương ứng residue 33 trên protein theo quy tắc này. Đây là ánh xạ cần kiểm với trình tự tham chiếu, không phải bảo đảm mọi id đều khớp: audit gặp 2 ca không khớp trong 130 peptide có trình tự thật để kiểm; loader bão hòa loại trường hợp bất nhất.

### 5.2 Mỗi dòng bảng PSI là một construct

| Cột             | Ý nghĩa                                          |
| ---------------- | -------------------------------------------------- |
| `id`           | Định danh construct theo mẫu ở trên           |
| `psi`          | Điểm ổn định suy từ 6 bin                    |
| `sum`          | Tổng count đã chuẩn hóa, dùng lọc độ sâu |
| `nb1`…`nb6` | Count đã chuẩn hóa của từng bin              |

**Construct** là phiên bản trình tự được tạo để đưa vào thí nghiệm. Một dòng có PSI chưa phải một dòng có ΔPSI: phải ghép được WT đúng điều kiện rồi mới trừ.

Đếm trực tiếp trong lần kiểm 21/10/2026, không tính dòng header:

| File trong `data/processed/` | Số dòng | Số dòng `sum ≥10` | Số peptide xuất hiện |
| ------------------------------ | --------: | ---------------------: | ----------------------: |
| `psi-rep1.tsv`               |   261.868 |                256.711 |                   9.590 |
| `psi-rep2.tsv`               |   261.999 |                256.920 |                   9.586 |
| `psi-sat_a.tsv`              |   134.608 |                132.231 |                     249 |
| `psi-sat_b.tsv`              |   134.563 |                131.771 |                     249 |
| `psi-wt.tsv`                 |   264.036 |                259.232 |                   9.614 |

Số peptide ở cột cuối tính trước lọc `sum`. Số dòng sau lọc còn bao gồm WT hoặc ô giữ nguyên amino acid; không phải số mẫu đột biến cuối cùng. Nếu dùng `wc -l`, kết quả lớn hơn số dòng dữ liệu 1 vì có header.

`psi-wt.tsv` là **điều kiện BAG6 WT**, không phải danh sách WT chung cho mọi thí nghiệm. Phân biệt **WT trình tự** với **WT kiểu gene BAG6 của tế bào**.

## 6. Nhãn cuối được dựng như thế nào?

### 6.1 Bộ quét: WT đo riêng

Loader quét hiện tại:

1. Đọc `psi-rep1.tsv`, giữ PSI hữu hạn và `sum ≥10`.
2. Lấy PSI WT từ `_mut0` của cùng peptide, trong cùng điều kiện.
3. Chỉ giữ peptide có PSI WT ≤3.
4. Lấy trình tự và amino acid thay vào từ CSV tác giả, kiểm độ dài và ký tự ở vị trí xét.
5. Tính ΔPSI từng vị trí; chỉ giữ peptide có ≥21 vị trí hợp lệ.

**[ĐO lại]** Kết quả: **2.994 peptide / 2.474 accession / 1.985 cụm cov80 / 83.446 ô**. Không bắt buộc mỗi peptide phải có vị trí dương.

Con số **2.624 footprint** thuộc phép đếm lịch sử trong [count_footprints.py](../../topics/degron-footprint/research/e3-labels-audit/count_footprints.py), đọc CSV và thêm điều kiện có ít nhất một vị trí ΔPSI ≥1. Số **2.402 khu trú** thêm điều kiện số vị trí dương ≤6. Các tập có logic lọc và kiểm trình tự khác nhau; không trừ 2.624 khỏi 2.994 rồi gọi phần còn lại là số peptide không có footprint.

Quy tắc thay thế quét thường gặp là `AGVLISTCDE → R`, `MWFP → S`, `YNQKRH → A`. Sổ dữ liệu ghi ngoại lệ, nên đọc amino acid thực tế từ trình tự construct; đừng sinh lại mutant bằng quy tắc một cách mù quáng.

### 6.2 Bộ bão hòa: WT nội tại riêng cho mỗi replicate

Không có `_mut0`. Tại vị trí i, ô thay vào đúng amino acid WT giữ nguyên trình tự protein. Repo gọi các ô này là ô “đồng nghĩa”; khi chỉ nhìn bảng PSI, cách nói chính xác nhất là **ô giữ nguyên amino acid**. Không cần suy đoán codon cụ thể để dùng chúng làm mốc.

Với mỗi peptide:

```text
WT_A = median(PSI của các ô giữ nguyên amino acid, nửa A)
WT_B = median(PSI của các ô giữ nguyên amino acid, nửa B)
WT để lọc peptide = (WT_A + WT_B)/2

Δ_A(i,a) = PSI_A(i,a) − WT_A
Δ_B(i,a) = PSI_B(i,a) − WT_B
y(i,a)   = [Δ_A(i,a) + Δ_B(i,a)]/2
```

Các ô dùng trong phép tính đã qua `sum ≥10`. Phải có **ít nhất 10 ô giữ nguyên amino acid ở mỗi nửa** để dựng hai mốc. Sau kiểm trình tự, chỉ giữ peptide có WT trung bình ≤3; chỉ giữ ô thay thế thật, hợp lệ, xuất hiện ở **cả hai nửa**. Loader này không gọi điều kiện ≥21 vị trí của bộ quét.

**[ĐO lại]** Kết quả: **91 peptide / 91 accession / 89 cụm cov80 / 47.847 ô**. Tối đa lý thuyết là 91×532 = 48.412 ô; 565 ô còn lại không nằm trong giao ô hợp lệ. Không điền chúng bằng 0: thiếu phép đo khác với đo được hiệu ứng bằng 0.

Ví dụ thật được đọc lại:

```text
Peptide: O00468_AGRN_82
WT seq:  SAGDVDTLAFDGRTFVEYLNAVTESELA
WT_A:    2.8765728625
WT_B:    2.8799374625
Số ô thay thế hợp lệ: 532
```

Nhãn 532 ô của peptide này được tính lại từ loader và khớp `y` trong cache G2 bằng `np.allclose`. Đây là kiểm tái tính trên dữ liệu hiện có, không phải thực hiện lại thí nghiệm tế bào.

Các mốc 249 peptide thô, 248 qua một audit cũ, 235 dựng ma trận và 91 sau lọc G2 có tiêu chí khác nhau. Luôn ghi kèm **bước xử lý** khi nói số peptide; không coi chúng là bốn phiên bản mâu thuẫn của cùng một phép đếm.

## 7. Tự đọc và tái dựng ΔPSI cho một peptide

Chạy từ gốc repo. Các lệnh dưới đọc dữ liệu hiện có, không tải hoặc dựng lại bảng PSI. `python -I` hạn chế ảnh hưởng import từ môi trường; nó không phải sandbox bảo mật. Chỉ nhập code nội bộ đã kiểm, không chạy code trong `data/raw/`.

### 7.1 Mở bảng và xem schema

```bash
head -5 topics/degron-footprint/data/processed/psi-sat_a.tsv
wc -l topics/degron-footprint/data/processed/psi-*.tsv
```

### 7.2 Dựng đầy đủ nhãn và ma trận 28×20

Đoạn sau nhập loader nội bộ bằng đường dẫn tuyệt đối, lấy peptide đầu tiên theo thứ tự id và tự kiểm nhãn tương ứng trong cache. Không cần `allow_pickle=True` vì cache hiện tại chỉ chứa các mảng số và chuỗi.

```bash
.venv/bin/python -I - <<'PY'
from pathlib import Path
import importlib.util
import numpy as np
import pandas as pd

root = Path.cwd()
topic = root / 'topics/degron-footprint'
path = topic / 'research/residue-task-derisk-2026-10-15/residue_data.py'
spec = importlib.util.spec_from_file_location('rd', path)
rd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rd)
data = rd.load_all()

pep = sorted(data['sat'])[0]
v = data['sat'][pep]
seq = v['seq']
matrix = np.full((28, 20), np.nan)
labels = []
for (pos, aa), (da, db) in sorted(v['cells'].items()):
    delta = (da + db) / 2
    matrix[pos - 1, rd.AAS.index(aa)] = delta
    labels.append(delta)

table = pd.DataFrame(matrix, index=range(1, 29), columns=list(rd.AAS))
print('Peptide:', pep)
print('WT:', seq)
print('WT riêng A/B:', v['wt_internal'])
print('Số ô:', len(labels))
print(table.round(2).to_string())

with np.load(topic / 'data/processed/g2-saturation-input.npz',
             allow_pickle=False) as z:
    i = list(z['peps']).index(pep)
    start, stop = z['idx'][i]
    np.testing.assert_allclose(labels, z['y'][start:stop])
    print('PASS: ΔPSI tự dựng khớp nhãn cache G2')
PY
```

Ô giữ nguyên amino acid và ô thiếu phép đo đều để `NaN` trong bảng này vì chúng không nằm trong nhãn thay thế thật của G2. Muốn phân biệt hai loại, đối chiếu cột với `seq[pos-1]`. Đừng hiểu toàn bộ `NaN` là “dữ liệu thí nghiệm bị mất”.

### 7.3 Đọc heatmap như thế nào?

Nếu muốn vẽ, thêm đoạn sau **bên trong khối Python ở trên**, sau khi đã có `table`, `seq`, `pep`. Nó ghi một PNG mới vào thư mục tạm riêng và in đường dẫn:

```python
import tempfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(11, 10))
cmap = plt.get_cmap('coolwarm').copy()
cmap.set_bad('#dddddd')
limit = max(1.0, float(np.nanmax(np.abs(matrix))))
im = ax.imshow(matrix, cmap=cmap, vmin=-limit, vmax=limit, aspect='auto')
ax.set_xticks(range(20), list(rd.AAS))
ax.set_yticks(range(28), [f'{i+1} {aa}' for i, aa in enumerate(seq)])
ax.set_xlabel('Replacement amino acid')
ax.set_ylabel('Position and WT amino acid')
ax.set_title(pep)
fig.colorbar(im, ax=ax, label='Delta PSI (mean A/B)')
fig.tight_layout()
outdir = Path(tempfile.mkdtemp(prefix='degron-dataset-guide-'))
output = outdir / 'delta-psi-heatmap.png'
fig.savefig(output, dpi=160)
plt.close(fig)
print(output)
```

Mỗi hàng là một vị trí; mỗi cột là amino acid thay vào. Màu phía dương cho thấy thay thế làm reporter bền hơn. Nếu nhiều thay thế ở một hàng cùng dương mạnh, vị trí đó nhạy với nhiều kiểu thay thế. Nếu chỉ một vài cột dương, kết luận phụ thuộc loại thay thế. Không gộp hàng thành một nhãn vị trí khi chưa công bố quy tắc gộp.

## 8. Hiểu cache G2 và 181 đặc trưng

```bash
.venv/bin/python -I - <<'PY'
import numpy as np
path = 'topics/degron-footprint/data/processed/g2-saturation-input.npz'
with np.load(path, allow_pickle=False) as d:
    for k in d.files:
        print(k, d[k].shape, d[k].dtype)
    assert np.isfinite(d['X']).all() and np.isfinite(d['y']).all()
    assert len(set(d['groups'])) == 89
PY
```

**[ĐO lại]** Schema thực tế:

| Mảng      | Shape        | Nội dung                                                             |
| ---------- | ------------ | --------------------------------------------------------------------- |
| `X`      | (47847, 181) | Mỗi dòng một ô thay thế, các đặc trưng ở dưới             |
| `y`      | (47847,)     | ΔPSI trung bình A/B                                                 |
| `idx`    | (91, 2)      | Khoảng `[start, stop)` của từng peptide trong các mảng mức ô |
| `peps`   | (91,)        | Id của từng peptide                                                 |
| `groups` | (91,)        | Đại diện cụm protein của từng peptide                           |
| `rowg`   | (47847,)     | Cụm protein của từng dòng mức ô                                 |
| `seqs`   | (47847,)     | Trình tự mutant                                                     |
| `wt`     | (47847,)     | **Chuỗi WT**, không phải PSI WT                              |

Cache không lưu trực tiếp cột vị trí và amino acid thay vào. Có thể phục hồi từ khác biệt `seqs`/`wt`, hoặc dùng thứ tự ô trong loader như mục 7.

181 cột gồm:

| Khoảng cột Python | Số chiều | Nội dung                                                                               |
| ------------------- | ---------: | --------------------------------------------------------------------------------------- |
| `0:20`            |         20 | One-hot amino acid WT tại vị trí thay                                                |
| `20:40`           |         20 | One-hot amino acid mutant                                                               |
| `40:60`           |         20 | Tần suất 20 amino acid trong peptide WT                                               |
| `60:180`          |        120 | One-hot 6 láng giềng theo thứ tự −3, −2, −1, +1, +2, +3; mỗi vị trí 20 chiều |
| `180`             |          1 | ΔPAP đóng băng = PAP(mutant) − PAP(WT) theo baseline của runner                   |

One-hot là vector có một phần tử bằng 1 đại diện ký tự tương ứng. Ngữ cảnh ngoài biên peptide được để vector 0. **Ridge M3 chỉ dùng 180 cột đầu**; có 181 cột trong cache không có nghĩa mọi mô hình đều dùng cả 181. Không đưa PSI WT thực nghiệm vào đầu vào của runner G2.

## 9. Vì sao phải chia theo cụm protein?

47.847 ô không phải 47.847 quan sát sinh học độc lập. Hàng trăm ô của cùng peptide dùng chung phần lớn trình tự và cùng mốc WT. Nhiều tile của cùng protein còn có thể chồng nhau; protein khác nhau có thể tương đồng trình tự.

Nếu chia ngẫu nhiên theo ô, train có thể chứa gần như toàn bộ một peptide và test chỉ chứa vài mutant còn lại của chính peptide đó. Câu hỏi lúc ấy khác với “mô hình có tổng quát hóa sang nhóm protein chưa thấy không?”.

G2 dùng accession → cụm MMseqs2 **id30/cov80** → 5 outer fold. Cụm này được dựng theo ngưỡng identity 30% và coverage của quy trình ghim; file [protein-id30-cov80_cluster.tsv](../../topics/degron-footprint/data/interim/protein-id30-cov80_cluster.tsv) gồm đại diện và thành viên. Cụm không tự bảo đảm loại mọi quan hệ sinh học hoặc mọi overlap với tập tiền huấn luyện.

```text
protein → cụm protein → outer train/test
ô của peptide → kế thừa cụm của protein
outer train → chia tiếp inner train/validation theo cụm
```

Outer test dùng để lấy dự đoán OOF, tức mỗi ô được dự đoán bởi mô hình của fold không học nhãn ô đó. Inner validation chọn alpha ridge hoặc epoch mạng. Ba seed **17, 29, 43 dùng cùng outer partition**; không gọi là ba lần chia outer độc lập.

Nếu phối hợp quét và bão hòa, phải kiểm giao peptide, protein và cụm giữa hai nguồn. Audit cũ thấy 130 peptide có mặt ở cả hai bộ; chỉ giữ cùng peptide một phía vẫn chưa đủ nếu protein họ hàng còn rò qua phía kia. Runner G2 hiện tại không đưa nhãn quét vào huấn luyện.

Bootstrap lấy mẫu lại **cụm**, giữ các peptide thuộc cụm cùng nhau, để không xem từng ô là một bằng chứng độc lập. Cov50 là cấu hình phân cụm khác phục vụ kiểm độ nhạy, không phải tên khác của cov80.

## 10. Độ tin cậy nhãn và ý nghĩa của “trần đo lường”

Các số sau là đọc từ audit đã lưu, chưa chạy lại toàn bộ phân tích tương quan trong lần viết này:

| Số liệu                                         | Quần thể/điều kiện                                                       | Nguồn                                                                                                                                                                                          |
| ------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pearson PSI A/B = 0,9544                          | 110.544 id có `sum ≥100` ở cả hai nửa                                  | [saturation-audit.json](../../topics/degron-footprint/research/full-data-audit/saturation-audit.json)                                                                                            |
| Pearson ΔPSI A/B = 0,8335                        | 122.412 ô thay thế chung thuộc 235 peptide dựng ma trận, theo audit đó | [saturation-matrix.json](../../topics/degron-footprint/research/full-data-audit/saturation-matrix.json)                                                                                          |
| Nhiễu khoảng 16,7% phương sai ΔPSI quan sát | Ước lượng cho một nửa trên tập của audit ma trận                    | Cùng file trên                                                                                                                                                                                |
| AUROC A chấm nhãn B = 0,9519                    | Macro theo peptide, tập bão hòa 91 peptide của pipeline derisk            | [ceiling.json](../../topics/degron-footprint/research/residue-task-derisk-2026-10-15/ceiling.json), [code tính](../../topics/degron-footprint/research/residue-task-derisk-2026-10-15/derisk.py) |

Không lấy tương quan PSI trên toàn bộ construct thay cho tương quan ΔPSI; phép trừ WT đưa thêm độ bất định vào nhãn.

Trong `derisk.py`, phép tính 0,9519 là dùng ΔPSI_A làm score và `ΔPSI_B ≥1` làm nhãn. Đây là mốc trả lời: **“một lần đo dự báo nhãn gọi từ lần đo kia tốt đến đâu?”** Nó không trực tiếp trả lời “mô hình tốt nhất có thể học từ sequence đạt bao nhiêu”.

Đặc biệt, benchmark mô hình dùng nhãn trung bình A/B, còn phép đối chiếu hai nửa dùng nhãn B. Hai phép chấm có mục tiêu khác nhau. Vượt mốc 0,9519 không tự chứng minh rò rỉ; cần kiểm protocol và nhãn. Ngược lại, ở xa mốc đó không tự chứng minh khoảng cách còn lại đều là ngữ cảnh có thể học.

Ước lượng nhiễu từ hai replicate thường dựa trên giả định sai số tương đương, độc lập và không thiên lệch. Các sai lệch chung cho cả hai lần đo không dễ lộ ra qua tương quan. Không diễn giải 16,7% thành “16,7% nhãn sai”, hoặc suy ra mô hình chắc chắn đạt 83,3% accuracy.

## 11. Các bẫy cần kiểm trước khi kết luận

1. **Đọc sai chiều PSI.** Với Zhang, thấp là kém bền. Bài 2 cũ hiện ghi ngược; ưu tiên code và bảng định nghĩa trong hướng dẫn này.
2. **Dùng nhầm `psi-wt.tsv`.** Đó là nền BAG6 WT. WT của quét là `_mut0` cùng điều kiện; WT của bão hòa là mốc nội tại riêng A/B.
3. **Lỗi header từ tác giả.** Ba id `A0A0B4J1Y8_IGLV9-49_1_mut{10,17,24}` bị ảnh hưởng. Bảng dựng lại đã sửa. [psi-build.json](../../topics/degron-footprint/research/full-data-audit/psi-build.json) lưu so 261.865 giá trị, sai khác lớn nhất khoảng 5×10⁻⁷, với quy tắc xử lý lỗi được ghi rõ.
4. **Gộp mọi con số thành một cỡ mẫu.** Id thiết kế, dòng có read, dòng đủ độ sâu, ô có ΔPSI và ô vào G2 là các tầng khác nhau.
5. **Điền thiếu bằng 0.** Một mutant không đo được không phải mutant đã chứng minh không ảnh hưởng.
6. **Gọi một vị trí âm từ một thay thế quét.** Một thay thế không đạt ngưỡng không đại diện cho cả 19 thay thế khác.
7. **Chỉ đánh giá peptide đã có footprint.** Đó là quần thể đã chọn có tín hiệu; chỉ số không mô tả mọi peptide hoặc toàn proteome.
8. **Bỏ qua overlap của baseline tiền huấn luyện.** Checkpoint Degformer công bố có WT của 91/91 peptide và 42.163/47.847 mutant trùng exact sequence với training data. Điểm 0,9248 không phải clean holdout. Nguồn: [results.json](../../topics/degron-footprint/research/g2-saturation-2026-10-18/results.json).
9. **Dùng kết quả cũ thay trạng thái hiện hành.** G2-extension có Degformer huấn luyện lại cùng nhãn dưới cov80, AUROC khoảng 0,7500 nhưng chỉ một seed; đó khác với checkpoint công bố và chưa là đối chứng tiền huấn luyện sạch cụm đầy đủ. Xem [e3-degformer-arch.json](../../topics/degron-footprint/research/g2-extension-2026-10-18/e3-degformer-arch.json).
10. **Đồng nhất endpoint khác nguồn.** Điểm tile, độ dồi dào protein, nhãn degron curate và pathogenicity không tự cùng nghĩa với ΔPSI reporter.

Trạng thái nghiên cứu mới nhất được ghi trong khối ngày 21/10 của [topic-decision.md](../../topics/degron-footprint/research/topic-decision.md). Các README lịch sử còn liên kết tới `DECISIONS.md`/`log.md` đã xóa; không cần khôi phục chúng để học dữ liệu. Vượt mốc baseline bằng ridge không đồng nghĩa đã chứng minh kiến trúc mới hoặc hoàn tất G2.

## 12. Lộ trình đọc và câu tự kiểm

### Buổi 1: hiểu phép đo và tự dựng một nhãn

1. Đọc mục 2–3, tự giải thích PSI WT =2,2 và PSI mutant =3,7.
2. Đọc mục 4–5, mở bảng PSI bằng `head`, chỉ ra đơn vị của một dòng.
3. Đọc mục 6, vẽ hai luồng WT: quét và bão hòa.
4. Chạy mục 7, xem một hàng trong ma trận và xác định ô giữ nguyên amino acid.

### Buổi 2: hiểu tập học và phép đánh giá

1. Chạy mục 8, giải thích `idx`, `groups`, `rowg`, `wt`.
2. Đọc mục 9–10, mô tả vì sao không chia ngẫu nhiên theo ô và vì sao 0,9519 không phải cận tuyệt đối.
3. Mở [protocol G2](../../topics/degron-footprint/research/g2-saturation-2026-10-18/PROTOCOL.md), rồi [runner](../../topics/degron-footprint/research/g2-saturation-2026-10-18/run.py).
4. Đọc [README G2](../../topics/degron-footprint/research/g2-saturation-2026-10-18/README.md) cùng phần cập nhật hiện hành ở `topic-decision.md`; phân biệt kết quả phát triển và kết luận nghiên cứu.

**Câu tự kiểm, chưa phải đánh giá mức thành thạo:**

- Vì sao ΔPSI +1,5 là làm reporter bền hơn nhưng có thể là làm degron yếu đi?
- Vì sao 28×20 ô thiết kế chỉ cho tối đa 532 phép thay thế thật?
- Vì sao không lấy `psi-wt.tsv` làm WT cho mọi peptide?
- 47.847 ô nằm trong bao nhiêu peptide và cụm? Đơn vị bootstrap là gì?
- Vì sao không suy ra số peptide không có footprint bằng 2.994−2.624?
- Nếu mô hình vượt AUROC giữa hai lần đo, cần kiểm gì trước khi kết luận?
- Muốn dùng ClinVar làm đánh giá ngoài, phải giải quyết sự khác nhau nào về endpoint?

### Khi muốn dựng lại toàn bộ pipeline

[data/README.md mục 6](../../topics/degron-footprint/data/README.md#6-dựng-lại-từ-đầu) có lệnh tải và tái dựng. Đây là thao tác **có ghi file**, khác với các bước đọc ở trên. `build_psi.py --condition all --validate` ghi lại bảng PSI và báo cáo; `g2-saturation-2026-10-18/audit.py` ghi lại `audit.json`. Khi thực hiện phải theo quy định sổ nguồn gốc trong `CLAUDE.md`, bảo toàn snapshot và ghi nhật ký xử lý. Học đọc dữ liệu chưa cần chạy lại các bước này.

## 13. Phạm vi kiểm chứng của tài liệu

**Đã thực hiện trong lần viết:** đọc quy định repo; đọc code dựng PSI, loader, tạo đặc trưng, runner, audit; đếm lại 5 bảng PSI; gọi loader cho cả quét và bão hòa; kiểm shape/dtype cache, tính hữu hạn của `X`/`y`; tái tính nhãn peptide ví dụ và so với cache.

**Đọc từ kết quả lưu, không đo lại trong lần viết:** tương quan replicate, ước lượng nhiễu, AUROC giữa hai lần đo, số liệu PAP/Degformer, các quy mô Voutsinos/Larsen/MaveDB/CRISPR/MetaDegron. Mỗi nhóm đã có liên kết audit ở mục tương ứng. Không tải nguồn mới, không huấn luyện lại, không tái tạo nhãn trong `data/`.
