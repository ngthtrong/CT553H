# Schulze & Lindorff-Larsen 2026 — ảnh hưởng của thay thế residue lên độ dồi dào protein

> *eLife* 13, 28/05/2026. DOI [10.7554/eLife.103721](https://doi.org/10.7554/eLife.103721) · PMID 42207673 ·
> PMC13218725. Tra qua PubMed ngày 14/10/2026. **[đã đọc]** toàn văn.
> Cùng nhóm Lindorff-Larsen với [Voutsinos 2026](voutsinos-2026.md) và QCDPred.

## Họ làm gì

Gộp **6 thí nghiệm VAMP-seq**, **31.614** điểm biến thể trên **PTEN, TPMT, NUDT15, CYP2C9, ASPA, PRKN** —
tất cả cùng **một phenotype** (độ dồi dào trong tế bào) và cùng một loại assay. Từ đó dựng **ma trận thay
thế amino acid** mô tả ảnh hưởng trung bình lên độ dồi dào theo **bối cảnh cấu trúc**.

Kết quả chính: ma trận dự đoán độ dồi dào **chính xác đến mức đáng ngạc nhiên** khi chỉ cho nó biết residue
**bị chôn hay phơi lộ**. Các tác giả đề nghị dùng ma trận của họ làm **baseline mạnh** cho mọi mô hình độ
dồi dào về sau.

## Chi tiết phương pháp đáng dùng

| Thứ | Cách họ làm |
|---|---|
| Ngưỡng chôn/phơi lộ | rASA **0,1**, chọn bằng grid search tối đa hóa Pearson trong **leave-one-protein-out CV** |
| Đặc trưng cấu trúc | rASA **và WCN** (weighted contact number) — WCN bù cho chỗ rASA không phân giải được bên trong lõi |
| Cấu trúc dùng | **Thực nghiệm**, và **homodimer** cho NUDT15 và ASPA (monomer phân loại sai residue ở mặt tiếp xúc) |
| Không dùng | pLDDT (vì dùng cấu trúc thực nghiệm) |
| Đối chứng | **ThermoMPNN ΔΔG**; ma trận và ΔΔG xếp hạng biến thể ngang nhau |
| rASA một mình | Spearman **0,45** trung bình với độ dồi dào (**0,54** nếu bỏ ASPA); WCN 0,41 (0,43) |

## Vì sao quan trọng với đề tài

1. **Hai đối chứng bắt buộc.** Ma trận theo lớp phơi lộ và ThermoMPNN ΔΔG phải có trong bảng kết quả của
   bất kỳ phần nào dùng nhãn độ dồi dào protein nguyên vẹn. rASA một mình (ρ 0,45) đã mạnh hơn ΔPAP ở
   khoảng phơi lộ nhất (0,3733, đo ngày 14/10).
2. **Họ tự nêu khoảng trống đúng là hướng của đề tài.** Framework cấu trúc đơn giản của họ **không bắt được**
   các cơ chế cần máy phân hủy, trong đó có **neo-degron ở vị trí phơi lộ**; các chỗ lệch "có thể dùng để
   định hướng phát triển mô hình độ dồi dào sau này, ví dụ bằng cách đưa vào đặc trưng sinh hóa phức tạp
   hơn". Đây là **lời mời trực tiếp**, dùng được làm dẫn nhập.
3. **Ca cụ thể để kể: PRKN S109.** Một residue **phơi lộ** nhưng profile thay thế giống residue **chôn** —
   phù hợp với việc đột biến ở đó tạo **degron chất lượng-kiểm soát phơi lộ**. Đúng loại hiện tượng mà mô
   hình degron phải bắt mà mô hình cấu trúc thuần không bắt được.
4. **Hai lỗi của repo mà bài này phát hiện ra.** Phép đo ngày 14/10 trộn bộ **GCK** (đo bằng DHFR-PCA, không
   phải VAMP-seq) và dùng AlphaFold **monomer** cho NUDT15/ASPA là homodimer. Phải chạy lại — xem
   [prior-art-exposure-gate §3](../../../topics/degron-footprint/research/architecture-check/prior-art-exposure-gate.md).

## Khác gì đề tài

Họ dự đoán **độ dồi dào của biến thể protein nguyên vẹn** từ **bối cảnh cấu trúc**; đề tài dự đoán **residue
nào trong degron quyết định độ bền** từ **trình tự peptide**, trên nhãn đột biến bão hòa. Khác cả đầu vào,
đầu ra và nguồn nhãn. Nhưng hai bên gặp nhau ở chỗ: cùng dùng nhãn VAMP-seq/MaveDB làm kiểm tra ngoài, và
cùng kết luận rằng mức phơi lộ quyết định cơ chế nào chi phối.
