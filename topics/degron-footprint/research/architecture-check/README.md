# Kiểm tiền đề kiến trúc MIL-Degron

> Ngày **14/10/2026**. Script: [architecture_check.py](architecture_check.py) →
> [architecture-check.json](architecture-check.json).
> Trả lời rủi ro ghi ở [thẻ đề tài](../../README.md): "kiến trúc MIL/cổng cấu trúc trong các trang cũ
> **chưa được kiểm chứng**". Kiểm **tiền đề** của hai thành phần bằng dữ liệu đã có;
> **không huấn luyện mô hình nào**, nên đây **không** phải bằng chứng kiến trúc sẽ thắng.
>
> ⚠️ **Đọc kèm [prior-art-exposure-gate.md](prior-art-exposure-gate.md) (tra y văn 14/10).** Lần tra đó cho
> thấy tiền đề ở mục 1 **đã được công bố nhiều lần**, và hiện tượng đổi dấu **Larsen 2025 đã tìm ra trên
> CRX**. Nó cũng phát hiện **hai lỗi phương pháp** của mục 1: tập có lẫn GCK (đo bằng DHFR-PCA, không phải
> VAMP-seq) và rASA tính trên AlphaFold **monomer** cho NUDT15/ASPA là protein homodimer. **Chưa dùng con số
> +0,6625 vào tài liệu nào cho tới khi chạy lại.**

## Hai tiền đề được kiểm, và hai tiền đề vẫn chưa kiểm được

Kiến trúc đề xuất ở [topic-decision §5](../topic-decision.md) có năm thành phần. Phiên này kiểm **tiền
đề** của hai thành phần — tức điều kiện phải đúng để thành phần đó có lý do tồn tại:

| Thành phần | Tiền đề | Kiểm được? |
|---|---|---|
| 4 — cổng phơi lộ (rASA, pLDDT nhân vào logit attention) | Tín hiệu degron chỉ biểu hiện ở vùng phơi lộ của protein nguyên vẹn | **Có**, mục 1 — nhưng tiền đề này **đã có trong y văn**, xem [prior-art](prior-art-exposure-gate.md) |
| 3, 5 — attention gộp túi, hai đầu ra đa nhiệm | Nhãn đoạn và nhãn residue đo cùng một đại lượng nên chia sẻ được biểu diễn | **Có**, mục 2 |
| 1 — mỗi vị trí sinh một cửa sổ ứng viên motif | Cấu trúc túi hơn đầu hồi quy theo vị trí | **Không** — cần huấn luyện cả hai |
| 2 — embedding PLM mức residue | PLM hơn one-hot ở nhiệm vụ này | **Không** — cần huấn luyện; và cache mức residue 32,7 GB vượt RAM ([bench_esm](../voutsinos-2026-audit/README.md)) |

## Nhãn bằng chứng

- **[đo]** tự chạy trong phiên này. **[phân tích]** suy luận từ các số đó.
- Giữ nguyên quy ước: **không** nói "chưa ai dùng MIL", **không** nói "dùng cấu trúc là phần mới" —
  Larsen 2025 đã tính rASA/pLDDT từ AlphaFold2 kèm DSSP.

## Chạy lại

```bash
.venv/bin/pip install biopython
# cấu trúc AlphaFold: cần User-Agent, nếu không EBI trả 403
cd topics/degron-footprint/data/raw/alphafold
for a in P60484 P51580 Q9NV35 P45381 O60260 P35557 P11712 P33261; do
  curl -s -A "Mozilla/5.0" -o AF-$a-F1-model_v6.pdb \
    https://alphafold.ebi.ac.uk/files/AF-$a-F1-model_v6.pdb
done
.venv/bin/python topics/degron-footprint/research/architecture-check/architecture_check.py
```

SHA-256 của 8 file: `data/raw/alphafold/manifest.txt`. rASA tính bằng Shrake–Rupley (Biopython 1.88),
chuẩn hóa theo max ASA lý thuyết của Tien 2013; pLDDT đọc từ cột B-factor. Chạy ~4 phút.

## 1. Cổng phơi lộ: **tiền đề đúng, và hiệu ứng rất mạnh**

Phép kiểm: nếu tín hiệu degron chỉ biểu hiện ở vùng phơi lộ, thì ΔPAP — một mô hình degron **không biết
gì về cấu trúc** — phải tương quan với độ dồi dào protein nguyên vẹn **tốt hơn rõ** ở residue phơi lộ.
Dữ liệu: 6 protein bào tương của MaveDB có bộ điểm **độ dồi dào** (không dùng bộ hoạt tính), ΔPAP tính
trên cửa sổ 30 residue quanh biến thể, hạng chuẩn hóa trong từng gene rồi gộp. 33.718 biến thể missense
khớp trình tự AlphaFold.

| Vùng theo rASA | Spearman(ΔPAP, độ dồi dào) | n |
|---|---:|---:|
| chôn < 0,2 | **−0,1928** | 15.949 |
| 0,2–0,5 | +0,0695 | 10.775 |
| 0,5–0,7 | +0,2342 | 4.303 |
| **phơi lộ ≥ 0,7** | **+0,3733** | 2.691 |

| Vùng theo pLDDT | Spearman | n |
|---|---:|---:|
| **< 50 (vô định hình)** | **+0,3973** | 2.258 |
| 50–70 | +0,1675 | 1.019 |
| 70–90 | −0,0150 | 6.216 |
| ≥ 90 (gấp chắc chắn) | −0,1642 | 24.225 |

Hồi quy trên thang hạng, có hằng số riêng theo gene: `y ~ ΔPAP + rASA + ΔPAP×rASA`

| Hệ số | Giá trị | Bootstrap 95% |
|---|---:|---|
| ΔPAP | −0,1808 | — |
| rASA | +0,5038 | — |
| **ΔPAP × rASA** | **+0,6625** | **[0,627; 0,700]** |

**[đo]** Khoảng tin cậy của hệ số tương tác **không chứa 0**, cách xa.

**Phép kiểm độ nhạy — PRKN chiếm gần một nửa số residue phơi lộ, nên bỏ nó ra:** hiệu ứng **vẫn còn**,
yếu hơn. Spearman theo rASA: −0,1837 → +0,0835 → +0,1680 → +0,1294 (phơi lộ cao giảm so với khi có PRKN);
hệ số tương tác **+0,5990**, bootstrap [0,546; 0,648]. **[đo]** Nên kết luận không do một protein gây ra,
nhưng **độ lớn phụ thuộc protein nào có trong tập**.

**[phân tích] Năm điều rút ra, đã đối chiếu y văn:**

1. **Tiền đề của cổng phơi lộ đúng — nhưng đây là xác nhận lại, không phải phát hiện.** Voutsinos 2026
   (ρ = −0,47 trên 173 protein phơi lộ nhất; Kruskal–Wallis P = 5,4 × 10⁻⁶ cho ΔPAP ở vùng phơi lộ), Larsen
   2025 (\|r\| = 0,41 với rASA, 0,36 với pLDDT), QCDPred, DEGRONOPEDIA và JoGo đều đã báo quan hệ này. Đóng
   góp của phép đo này chỉ là **quy mô và loại nhãn**: 6 protein, 33.718 biến thể, nhãn độ dồi dào trực tiếp,
   kèm hệ số tương tác có khoảng tin cậy. Xem [prior-art-exposure-gate.md](prior-art-exposure-gate.md).
2. **Dấu đổi chiều ở vùng chôn — Larsen 2025 đã tìm ra trên CRX.** Họ báo ΔPAP Pearson **0,54** trong vùng
   vô định hình so với **−0,19** trong homeodomain đã gấp. Cùng chiều, cùng độ lớn. Phép đo ở đây mở rộng từ
   1 lên 6 protein và từ nhãn transactivation sang nhãn độ dồi dào. **Không được trình bày như phát hiện
   của đề tài.** Cách đọc cơ chế vẫn giữ: đột biến ở nhân làm mất gấp nên protein bị phân hủy, trong khi
   ΔPAP chỉ đọc thành phần cục bộ và có thể báo "bền hơn" — một mô hình degron không có cấu trúc **sai dấu**
   ở 47% residue.
3. **pLDDT phân tách mạnh hơn rASA** (+0,3973 so với −0,1642, cách nhau 0,56). Nên cổng dùng **cả hai**, và
   nếu chỉ chọn một thì pLDDT, vốn cũng rẻ hơn (không cần tính SASA). Lưu ý Schulze 2026 chọn hướng khác:
   họ thêm **WCN** vì rASA không phân giải được bên trong lõi; họ không dùng pLDDT vì dùng cấu trúc thực nghiệm.
4. **Hai lỗi phương pháp phải sửa trước khi dùng số.** (a) Bộ GCK (`urn:mavedb:00000096-b-1`) đo bằng
   **DHFR-PCA**, không phải VAMP-seq — trộn hai loại assay là đúng thứ Schulze 2026 cảnh báo, phải bỏ GCK.
   (b) NUDT15 và ASPA là **homodimer**; rASA tính trên AlphaFold monomer phân loại sai residue ở mặt tiếp
   xúc, Schulze 2026 dùng cấu trúc dimer cho đúng hai protein này. Phải chạy lại.
5. **Có baseline mạnh hơn mà đề tài chưa tính tới.** rASA **một mình** cho Spearman 0,45 trung bình (0,54 bỏ
   ASPA) với độ dồi dào — cao hơn ΔPAP ở khoảng phơi lộ nhất (0,3733). Ma trận thay thế theo lớp phơi lộ của
   Schulze 2026 và **ThermoMPNN ΔΔG** là hai đối chứng **bắt buộc** cho phần nào của đề tài dùng nhãn độ dồi
   dào. Chi tiết: [prior-art-exposure-gate.md §3](prior-art-exposure-gate.md).

**Giới hạn phải nói rõ:** đây là **tiền đề**, không phải kết quả kiến trúc. Nó nói "cấu trúc mang thông tin
mà mô hình degron hiện có bỏ sót", **không** nói "đặt cổng ở bước gộp sẽ thắng". Chỉ 6–7 protein; CYP2C9
(protein màng ER) cho hiệu ứng yếu hơn và CYP2C19 bị loại vì chỉ 5/121 biến thể khớp trình tự AlphaFold.

## 2. Nối nhãn đoạn với nhãn residue: **tiền đề đúng ở mức toàn cục, yếu ở mức trong-nhóm**

Phép kiểm: hai assay có đo cùng đại lượng không. So PSI hoang dã của peptide Zhang 2023 với điểm độ dồi
dào của tile Voutsinos 2026 chồng ≥ 20 residue.

| Phép đo | Giá trị |
|---|---:|
| Peptide Zhang có PSI hoang dã | 8.831 |
| Có tile Voutsinos chồng ≥ 20 residue | **2.726** |
| **Spearman, toàn bộ** | **0,7333** |
| Spearman, **chỉ trong nhóm peptide degron** (PSI WT ≤ 3) | **0,2921** (n = 1.000) |
| Peptide có footprint | 2.624 |
| … có tile Voutsinos | **770** |
| … có tile nằm trong **tập train của PAP** | **725** |

**[đo]**

**[phân tích] Ba hệ quả:**

1. **Hai assay đo cùng đại lượng, nên học đa nhiệm có cơ sở.** Spearman 0,7333 trên 2.726 peptide là cao,
   và hợp lý vì cả hai đều gắn peptide vào đầu C của GFP rồi đọc độ bền.
2. **Nhưng trong nhóm peptide degron thì chỉ 0,2921.** **[phân tích]** Nghĩa là nhãn đoạn phân biệt tốt
   "có degron hay không" mà phân biệt kém **mức độ** giữa các degron. Nhiệm vụ phụ trợ vì vậy nên được đặt
   là **phân loại** (có/không) hoặc có trọng số nhỏ, chứ không phải hồi quy ngang hàng với nhiệm vụ chính.
   Đây là một ràng buộc thiết kế cụ thể mà trước đây chưa có.
3. **Rủi ro rò rỉ chéo nhiệm vụ: 725/770 peptide footprint có tile trong tập train của PAP.** Nếu dùng
   nhãn đoạn làm nhiệm vụ phụ **và** báo ΔPAP làm đối chứng trên cùng tập test, phải nói rõ ΔPAP đã thấy
   gần như toàn bộ các peptide đó ở mức đoạn. Phần B của [pap-baseline](../pap-baseline/README.md) đã đo
   và thấy **không có lợi thế nào** (0,4268 so với 0,4270), nên trên thực tế rò rỉ này không làm sai lệch
   đối chứng — nhưng vẫn phải ghi trong thiết kế benchmark.

## Những gì **không** làm

- **Không** kiểm tính mới ở phiên đo (14/10 chiều); phần đó làm sau, ghi ở
  [prior-art-exposure-gate.md](prior-art-exposure-gate.md), và nó đã sửa lại kết luận của mục 1.

- **Không huấn luyện mô hình nào.** Mọi số là tiền đề đo trên nhãn và mô hình đã có.
- Không kiểm hai tiền đề còn lại (cấu trúc túi so với đầu hồi quy theo vị trí; PLM so với one-hot) — cả
  hai cần huấn luyện.
- Không tính rASA cho **peptide tách rời**: trong assay GPS peptide được coi là phơi lộ hoàn toàn, nên
  phép kiểm này chỉ nói về chế độ protein nguyên vẹn.
- Không dùng bộ điểm **hoạt tính** của MaveDB (PTEN lipid phosphatase, NUDT15 activity, GCK
  complementation, LDLR uptake) — chúng đo chức năng, không đo độ bền.
